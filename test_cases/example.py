from crawler import Crawler
from selenium import webdriver
import pandas as pd

# another use case for 'Crawler'

options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)

search_parameters = {
    "departureDate": None,
    "destinationAirportCode": None,
    "originationAirportCode": None,
    "scheduleViewType": None,
    "timeOfDay": None,
}


URL = "https://www.southwest.com/air/flight-schedules/results.html"


def define_trip(
        departure_date,
        destination,
        origin,
        schedule_view,
        time_of_day
):
    search_parameters["departureDate"] = departure_date
    search_parameters["destinationAirportCode"] = destination
    search_parameters["originationAirportCode"] = origin
    search_parameters["scheduleViewType"] = schedule_view
    search_parameters["timeOfDay"] = time_of_day
    return search_parameters


days = ["2021-03-03",
        "2021-03-04",
        "2021-03-05",
        "2021-03-06",
        "2021-03-07",
        "2021-03-08",
        "2021-03-09"]

DATA = []
for day in days:
    driver.implicitly_wait(100)
    define_trip(day, "BUR", "SFO", "daily", "ALL_DAY")
    query = "&".join([f"{k}={v}" for (k, v) in search_parameters.items()])
    ext_url = URL + "?" + query
    SWACrawler = Crawler(ext_url, options, driver)
    df = SWACrawler.to_dataframe(["dates", "times"],
                                       ["//*[@class='date-title']",
                                        "//*[@class='time--value']"], 1)

    DATA.append(df)

df = DATA[0]
for i in DATA[1:]:
    df = pd.concat([df, i], axis=1)
df.to_excel("Flights_Test.xlsx")
