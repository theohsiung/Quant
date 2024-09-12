import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Yahoo Finance搜尋關鍵字的URL，這裡是"2330"
# keyword = "2330"
# url = f"https://tw.stock.yahoo.com/quote/{keyword}.TW"
url = "https://tw.stock.yahoo.com/news"

# 發送HTTP GET請求以獲取搜尋結果頁面內容
response = requests.get(url)
response.raise_for_status()  # 檢查請求是否成功
soup = BeautifulSoup(response.text, 'html.parser')
# 找到包含新聞的部分
news_section = soup.find_all('li', class_='js-stream-content')
news_data = []

# 遍歷新聞項，提取標題、連結、日期和內容
for news_item in news_section:
    # 提取標題
    title = news_item.find('h3').text if news_item.find('h3') else None
    link = news_item.find('a')['href'] if news_item.find('a') else None
    if link and not link.startswith('http'):  # 檢查是否為完整的URL
        link = "https://finance.yahoo.com" + link

    # 提取日期
    date = news_item.find('time')['datetime'] if news_item.find('time') else None
    content = None

    # 如果存在連結，訪問該連結並抓取內容
    if link:
        article_response = requests.get(link)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # 提取文章內容，一般文章內容在<div>或<p>標籤中
        article_body = article_soup.find('div', class_='caas-body')
        if article_body:
            content = ' '.join([p.text for p in article_body.find_all('p')])
        time.sleep(1)

    # 將提取到的數據加入列表
    news_data.append([title, link, date, content])

df = pd.DataFrame(news_data, columns=['Title', 'Link', 'Date', 'Content'])
# csv_filename = f'yahoo_finance_news_{keyword}.csv'
csv_filename = f'yahoo_finance_news.csv'
df.to_csv(csv_filename, index=False)

print(f"News data has been saved to {csv_filename}")
