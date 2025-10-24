import pandas as pd
from urllib.parse import urlencode
import json
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

hymns = hymns[['displayTitle', 'authors', 'textAuthNumber']]

hymns = hymns.rename(columns={'displayTitle': 'title'})

hymns.replace({np.nan: None}, inplace=True)

# Retrieve texts
texts_url = "https://hymnary.org/files/hymnary/other/texts.csv"
texts = pd.read_csv(texts_url)

merged = pd.merge(hymns, texts[['textAuthNumber', 'yearsWrote']], on='textAuthNumber', how='left')

# File write and appending to JSON file
results = []
for _, row in merged.iterrows():
    title = str(row.get("title", "")).strip()
    authors = str(row.get("authors", "")).strip()
    pub_date = (
        str(row.get("yearsWrote", "")).strip()
        if pd.notna(row.get("yearsWrote"))
        else ""
    )

    results.append({
        "title": title,
        "authors": authors,
        "publicationDate": pub_date
    })


with open("data/hymns.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
