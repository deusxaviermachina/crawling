from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, URL, options, driver):
        self.URL = URL
        self.options = options
        self.driver = driver

    def inspect(self):
        url = self.driver.get(self.URL)
        data = BeautifulSoup(self.driver.page_source, "html.parser")
        print(data.prettify())
        return data

    def read_tables(self):
        url = self.driver.get(self.URL)
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

    def to_dataframe2xl(self, names, elements, filename):
        data = self.get_dict_object(names, elements)
        data = [j for i,j in sorted(data.items(), key=lambda x: len(x[1]), reverse=False)]
        data_list = [pd.DataFrame(data=item) for item in data]
        df = data_list[0]
        for i in data_list[1:]:
            df = df.append(i)
        df.to_excel(filename)
        return df

# test use case
if __name__ == "__main__":
    URL = "https://www.southwest.com/air/flight-schedules/results.html?departureDate=2021-03-04&destinationAirportCode=OAK&originationAirportCode=BOS&scheduleViewType=daily&timeOfDay=ALL_DAY"
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(options=options)
    c = Crawler(URL, options, driver)
    c.inspect()
    DF = c.to_dataframe2xl(["dates", "times"],
        ["//*[@class='date-title']",
         "//*[@class='time--value']"], "CASEFLIGHTSTEST.xlsx")
    print(DF)


