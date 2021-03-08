from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from crawler import Crawler

options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(options=options)

url = "https://weather.com/weather/tenday/l/USWA0538:1:US"

spider = Crawler(url, options, driver)

# inspect document for relevant data points (in this case it's dates, high temperatures, and low temperatures)

spider.inspect()

names = ["days", "high", "low"]

# extract data based on their xpath
elements = ["//h2[@class='DetailsSummary--daypartName--1Mebr']",
            "//span[@class ='DetailsSummary--highTempValue--3x6cL']",
            "//span[@class='DetailsSummary--lowTempValue--1DlJK']"
            ]

df = spider.to_dataframe(names, elements, 1)
df.to_excel("weather.xlsx")
