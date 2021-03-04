from crawler import Crawler, clean_sheet, reformat_sheet
from selenium import webdriver
import pandas as pd
import openpyxl as xl
from xl_manip import reformat_sheet, clean_sheet


# a somewhat more involved use case for 'Crawler'

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


days = ["2021-03-04",
        "2021-03-05",
        "2021-03-06",
        "2021-03-07",
        "2021-03-08",
        "2021-03-09",
        "2021-03-10"]


DATA = []

for day in days:
    driver.implicitly_wait(100)
    define_trip(day, "BUR", "SFO", "daily", "ALL_DAY")
    query = "&".join([f"{k}={v}" for (k, v) in search_parameters.items()])
    ext_url = URL + "?" + query
    SWACrawler = Crawler(ext_url, options, driver)
    elems = SWACrawler.get_dict_object(["dates", "times"],
                                       ["//*[@class='date-title']",
                                        "//*[@class='time--value']"])

    DATA.append(elems)

if __name__ == "__main__":
    df = pd.DataFrame(data=DATA)
    df.to_excel("BUR2SF_flights_3.03.2021_to_3.09.2021v9.xlsx")
    clean_sheet("BUR2SF_flights_3.03.2021_to_3.09.2021v9.xlsx")
    reformat_sheet("BUR2SF_flights_3.03.2021_to_3.09.2021v9.xlsx")
