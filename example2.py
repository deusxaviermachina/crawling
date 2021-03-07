from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from crawler import Crawler
import os
url = "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-43"
options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(options=options)
spider = Crawler(url, options, driver)
spider.inspect()
tables = spider.read_tables()

i = 0
if os.path.isdir("FBI_Data"):
    pass
else:
    os.mkdir("FBI_Data")

for table in tables:
    i += 1
    table.to_excel(f"FBI_Data/Table{i}.xlsx")