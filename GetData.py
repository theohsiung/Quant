import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
import os.path
import json
from bs4 import BeautifulSoup
import csv

def check_equal_lengths(lst):
    # 如果列表為空，則所有元素長度相同
    if not lst:
        return True
    
    # 取第一個元素的長度作為基準
    base_length = len(lst[0])
    
    # 檢查每個元素的長度是否與基準長度相同
    has_different_lengths = False
    for item in lst:
        if len(item) != base_length:
            has_different_lengths = True
            break
    
    # 如果所有元素的長度都相同，則返回 True
    if not has_different_lengths:
        return True
    
    # 儲存長度不同的行的索引
    different_lengths = []
    
    # 檢查每個元素的長度是否與基準長度相同
    for i, item in enumerate(lst):
        if len(item) != base_length:
            different_lengths.append(i)
    
    # 統計每個長度的出現次數
    length_counts = {}
    for item in lst:
        length = len(item)
        length_counts[length] = length_counts.get(length, 0) + 1
    
    # 打印出長度不同的行和其長度
    print("Rows with different lengths:")
    for index in different_lengths:
        row = lst[index]
        print(f"Row: {row}, Length: {len(row)}")
    
    # 打印出大部分長度以及其他長度
    max_length = max(length_counts.values())
    print("\nMost common length(s):")
    for length, count in length_counts.items():
        if count == max_length:
            print(f"Length: {length}, Count: {count} (most common)")
        else:
            print(f"Length: {length}, Count: {count}")

    # 如果存在不同長度的行，則返回 False，否則返回 True
    return False


class CrawlData:

    def __init__(self, start, end):
        self.start_date = start
        self.end_date = end
        self.date_list = []  # 初始化日期列表

    def GetDateList(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            self.date_list.append(current_date.strftime("%Y%m%d"))
            current_date += timedelta(days=1)

    def Exist(self, current_date, datapath):
        file = datapath + '/' + str(current_date) + '.csv'
        return os.path.isfile(file)  # 返回檔案是否存在的布林值

    def GetStockData(self, path):
        self.GetDateList()  # 呼叫取得日期列表的方法
        for day in self.date_list:
            if self.Exist(day, path) == True: #確定檔案不存在
                print(f'file already exists')
                continue

            url = f'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={day}&type=ALL&response=csv'
            try:
                response = requests.get(url)
            except Exception as e:
                assert False, f"{day} fail grabbing: {e}"
                continue

            data = response.text
           
            lines = data.strip().split('\n')
            parsed_data = [line.strip().strip('"').split('","') for line in lines]
            del parsed_data[0]

            output = []
            for row in parsed_data:
                length = len(row)
                # print(row)
                # print(row[0])
                flag ='="' in row[0]
                if length == 16 and not flag:
                    output.append(row)

            if len(output) == 0:continue

            try:
                df = pd.DataFrame(output[1:], columns=output[0])
                df.set_index('證券代號', inplace=True)
                # print(df)
                df.to_csv(f'./database/{day}.csv')
                print(f'save {day}')
                time.sleep(6)
            except Exception as e:
                print(output)
                assert False, f"{day} fail grabbing Tradding info: {e}"
                continue
            

    def ThreeMajor(self, m_path):
        self.GetDateList()

        for day in self.date_list:
            # 把 csv 檔抓下來
            if self.Exist(day, m_path) == True: #確定檔案不存在
                print(f'file already exists')
                continue
            # 把 csv 檔抓下來
            url = f'https://www.twse.com.tw/rwd/zh/fund/T86?date={day}&selectType=ALLBUT0999&response=html'

            while True: 
            #----------------------------------------------------------------------------------------------
                try:
                    res = requests.get(url)
                except Exception as e:
                    assert False, f"{day} fail grabbing 3M: {e}"
                    continue

                data = res.text
                soup = BeautifulSoup(data, 'html.parser')
                # Find table element
                table = soup.find('table')
                # Extract table headers
                try:
                    headers = [header.text.strip() for header in table.find_all('th')]
                except Exception as e:
                    print(f"{day} no data today due to holidays or weekend: {e}")
                    flag = True
                    break

                del headers[0]

                # Extract table data
                data = []
                for row in table.find_all('tr'):
                    row_data = [cell.text.strip() for cell in row.find_all('td')]
                    if row_data:
                        data.append(row_data)

                result = check_equal_lengths(data)
                if result == True: break
                else:
                    print("reloading data due to asymmetric data format")
                    time.sleep(5)
            #----------------------------------------------------------------------------------------------

            try:
                # Convert to DataFrame
                df = pd.DataFrame(data, columns=headers)
                # 將證券代號轉換為字串格式
                df['證券代號'] = df['證券代號'].astype(str)
                # 刪除不是數字的列
                df = df[df['證券代號'].str.isdigit()]

                df.to_csv('output.csv', index=False)
                df.set_index('證券代號', inplace=True)
                df.to_csv(f'./3Major/{day}.csv')
                print(f'save 3Major Exchange {day}')
                time.sleep(6)
            except Exception as e:
                if flag != True:
                    print(f"{day} fail grabbing 3M: {e}")
                    break
                continue
            



class GetData:
    def __init__(self, path):
        self.path = path

    def DataLoader(self, select_date):
        path = self.path
        filename = select_date + '.csv'
        file_path = os.path.join(path, filename)
        df = pd.read_csv(file_path)
        df.set_index('證券代號', inplace=True)
        return df
