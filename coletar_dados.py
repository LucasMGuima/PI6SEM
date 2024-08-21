import os
from datetime import datetime, timezone, timedelta, datetime

timezone_offset = -3.0  # Pacific Standard Time (UTC−03:00)
tzinfo = timezone(timedelta(hours=timezone_offset))
data = datetime.now(tzinfo)
data = f"{data.day}_{data.month}_{data.year}"
file = f'..\dados\{data}.csv'

os.chdir("./clima")
os.system(f"scrapy crawl clima -o {file} -t csv")