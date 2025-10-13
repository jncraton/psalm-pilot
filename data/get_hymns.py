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
hymn_titles = hymns['displayTitle', 'authors']

# export as .json
hymn_titles.to_json("hymns.json")
