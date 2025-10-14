import pandas as pd
from urllib.parse import urlencode

# import csv from Hymnary
# the url uses advanced search to filter for multiple things outlined in the params
base_url = "https://hymnary.org/search"

params = {
    "qu": "textLanguages:english denominations:church of god media:text "
    "textClassification:textispublicdomain tuneClassification:tuneispublicdomain in:texts",
    "sort": "totalInstances",
    "export": "csv",
    "limit": 100
}

query_string = urlencode(params)
url = f"{base_url}?{query_string}"

hymns = pd.read_csv(url)
hymns_data = hymns[['displayTitle', 'authors']]

# logic for if an author is not recorded so it doesn't show up as an error
hymns_data.fillna(value={"authors": "Author not recorded."}, inplace=True)

# export as .json
hymns_data.to_json("hymns.json", indent=2)