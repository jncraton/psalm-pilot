import pandas as pd
from urllib.parse import urlencode
import numpy as np

# import csv from Hymnary
# the url uses advanced search to filter for multiple things outlined in the params
base_url = "https://hymnary.org/search"

params = {
    "qu": {
        "textLanguages": "english",
        "denominations": "church of god",
        "media": "text",
        "textClassification": "textispublicdomain",
        "tuneClassification": "tuneispublicdomain",
        "in": "texts",
    },
    "sort": "totalInstances",
    "export": "csv",
    "limit": 100
}

params["qu"] = " ".join([f"{k}:{v}" for k, v in params["qu"].items()])
query_string = urlencode(params)
url = f"{base_url}?{query_string}"

hymns = pd.read_csv(url)
hymns = hymns.rename(columns={'displayTitle': 'title'})

hymns['popularity'] = (hymns['totalInstances'] / hymns['totalInstances'].max()).round(2)

hymns.replace({np.nan: None}, inplace=True)
        
# export to json
hymns = hymns[['title', 'popularity', 'authors']]
hymns.to_json("hymns.json", orient="records", indent=2)