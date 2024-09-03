from GetData import *
from datetime import datetime, timedelta
from Analysis import Analyzer

num_path = './database'
three_path = './3Major'

# analyzer = Analyzer('20240326' ,num_path)
# analyzer.KD('2330', 9)




# crawl data through Internet from start-date ~ end-date
start_date = datetime(2023, 9, 1)
end_date = datetime(2024, 4, 1)

# data crawlling
crawler = CrawlData(start_date, end_date)
# crawler.GetStockData(num_path)
crawler.ThreeMajor(three_path)
 
