import pandas as pd
from urllib.parse import urlencode
import numpy as np

# import csv from Hymnary
# the url uses advanced search to filter for multiple things outlined in the params
base_url = "https://hymnary.org/search"
# General database for identifying the years and to match authNums
texts_url = "https://hymnary.org/files/hymnary/other/texts.csv"

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
texts = pd.read_csv(texts_url)

hymns = hymns.merge(texts[['textAuthNumber', 'yearsWrote']], on='textAuthNumber', how='left')

hymns.replace({np.nan: None}, inplace=True)
hymns = hymns[['displayTitle', 'authors','yearsWrote']]
hymns = hymns.rename(columns={
    'displayTitle': 'title',
    'yearsWrote': 'publicationDate'
})

# export to json
hymns.to_json("data/hymns.json", orient="records", indent=2)
