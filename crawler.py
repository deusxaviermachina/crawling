from selenium import webdriver
import pandas as pd
from xl_manip import reformat_sheet, clean_sheet


class Crawler:
    def __init__(self, URL, options, driver):
        self.URL = URL
        self.options = options
        self.driver = driver
        
    def read_tables(self):
        try:
            data = pd.read_html(self.driver.page_source)
        except ValueError:
            print(f"no tables found for page {self.URL}")
            return
        return data

    def extract_elements(self, x_path: str, human_read=True) -> list:
        """
        extract relevant elements based on their xpath,
        and get a list of these elements
        """
        self.driver.get(self.URL)
        if human_read:
            elements = [i.text for i in self.driver.find_elements_by_xpath(x_path)]
        else:
            elements = self.driver.find_elements_by_xpath(x_path)
        return elements

    def get_dict_object(self, names: list, elements: list) -> dict:
        """
        for the key-value pairs, values are
         lists of n elements and keys are strings.
         'names' is a list of n strings
        """
        assert len(names) == len(elements)
        data = {}
        for (i, j) in zip(names, elements):
            elems = self.extract_elements(j)
            data[i] = elems

        return data


#test use case
if __name__ == "__main__":
    URL = "https://www.southwest.com/air/flight-schedules/results.html?departureDate=2021-03-04&destinationAirportCode=OAK&originationAirportCode=BOS&scheduleViewType=daily&timeOfDay=ALL_DAY"
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(options=options)
    c = Crawler(URL, options, driver)
    elems = c.get_dict_object(
        ["dates", "times"],
        ["//*[@class='date-title']",
        "//*[@class='time--value']"])
    DATA = []
    """
       pandas will throw an error if columns aren't of the same length--
       to prevent this, append elements to an empty list
    """
    DATA.append(elems)
    df = pd.DataFrame(data=DATA)
    filename = "FLIGHTS.xlsx"
    df.to_excel(filename)
    clean_sheet(filename)
    reformat_sheet(filename)


