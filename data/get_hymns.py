import pandas as pd
from urllib.parse import urlencode
import numpy as np

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
hymns = hymns[['displayTitle', 'authors']]

hymns.replace({np.nan: None}, inplace=True)
        
# export to json
hymns.to_json("hymns.json", orient="records", indent=2)