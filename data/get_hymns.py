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
hymns = hymns[['displayTitle', 'authors']]
hymns = hymns.rename(columns={'displayTitle': 'title'})

hymns.replace({np.nan: None}, inplace=True)

texts_url = "https://hymnary.org/files/hymnary/other/texts.csv"
texts = pd.read_csv(texts_url)

def normalize_title(title: str):
    return (
        str(title)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("!", "")
        .replace("?", "")
        .replace(",", "")
        .replace("'", "")
        .replace(":", "")
        .replace(";", "")
    )

hymns["normTitle"] = hymns["title"].apply(normalize_title)
texts["normTitle"] = texts["textAuthNumber"].astype(str).str.strip().str.lower()

merged = pd.merge(hymns, texts[["normTitle", "yearsWrote"]], on="normTitle", how="left")

results = []
for _, row in merged.iterrows():
    title = str(row.get("title", "")).strip()
    authors = str(row.get("authors", "")).strip()
    pub_date = (
        str(row.get("yearsWrote", "")).strip()
        if pd.notna(row.get("yearsWrote"))
        else "No Written Year found"
    )

    results.append({
        "title": title,
        "authors": authors,
        "publicationDate": pub_date
    })


with open("data/hymns.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
