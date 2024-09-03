import os
import numpy as np
import pandas as pd
from GetData import GetData
import datetime

'''如果股票當日交易資訊有該資料但法人資料中找不到代表三大法人皆沒有任何動作
    法人資料中有包含etf但股市當日交易資料中沒有，所以排除etf以股市交易資料為準去找法人資料
'''

class Analyzer:
    def __init__(self, c_date, data_path):
        self.current_date = c_date
        self.path = data_path
    
    def KD(self, stock_num, time_period):
        getter = GetData(self.path)

        # data for all stocks in current date
        current_date = datetime.datetime.strptime(self.current_date, "%Y%m%d")
        price_list =[]
        L_list = []
        H_list = []
        N_len = time_period
        while time_period > 0:
            try:
                # 將日期轉換為字串格式，並構建檔案名稱
                file_name = current_date.strftime('%Y%m%d')


                df = getter.DataLoader(file_name)
                end_price_info = df.loc[stock_num]['收盤價']
                end_price_info = float(end_price_info)
                H_price_info = df.loc[stock_num]['最高價']
                H_price_info = float(H_price_info)
                L_price_info = df.loc[stock_num]['最低價']
                L_price_info = float(L_price_info)
                #store info for current day
                if len(price_list) == 0:
                    today_price = end_price_info

                price_list.append(end_price_info)
                H_list.append(H_price_info)
                L_list.append(L_price_info)

                time_period -= 1
                current_date -= datetime.timedelta(days=1)

            except Exception as e:
                # 如果在日期遞減過程中出現異常，輸出錯誤消息並中止迴圈
                print(f'No data in {current_date} when analyzing:', e)
                current_date -= datetime.timedelta(days=1)
                continue
        
        print(price_list)
        print(today_price)

        RSV = (today_price-min(L_list))/(max(H_list)-min(L_list))*100
        K = (RSV + (N_len-1)*50)/N_len
        print(RSV)
            



