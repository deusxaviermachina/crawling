import pandas as pd
import re

def webpage_to_xl_csv(url, title, idx=0, file_extension="xlsx"):
    supported = [
        "xlsx",
        "xls",
        "csv",
    ]
    assert file_extension in supported
    table = pd.read_html(url)
    df = pd.DataFrame(table[idx], columns=[i for i in table[idx]])
    if re.match(r"^xls.", file_extension):
        return df.to_excel(f"{title}.{file_extension}")
    else:
        return df.to_csv(f"{title}.{file_extension}")

#example url
url = "https://www.ssa.gov/oact/STATS/table4c6.html"
#webpage_to_xl_csv(url, "testI", file_extension="xlsx")
#webpage_to_xl_csv(url, "testII", file_extension="csv")
