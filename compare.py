import pandas as pd

def compare_csv(file1, file2):
    # 讀取CSV檔案並轉換為DataFrame
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df1.set_index('證券代號', inplace=True)
    df2.set_index('證券代號', inplace=True)

    l1 = df1.index
    l2 = df2.index
    l2 = [str(x) for x in l2]

    l1_not_l2=[]
    l2_not_l1 = []


    for i in l1:
        if i not in l2:l1_not_l2.append(i)
    for i in l2:
        if i not in l1:l2_not_l1.append(i)


    return l1_not_l2, l2_not_l1


if __name__ == "__main__":
    file1 = './database1/20240329.csv'
    file2 = './3Major/20240329.csv'

    diff1, diff2 = compare_csv(file1, file2)
    print("第一個檔案中有，但第二個檔案中沒有的索引 (三大法人皆沒買進)：", diff1)
    print("第二個檔案中有，但第一個檔案中沒有的索引 （ETF）：", diff2)
    print(len(diff2))
