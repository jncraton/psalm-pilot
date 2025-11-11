from urllib.parse import urlencode
from urllib.request import urlopen
from html.parser import HTMLParser
import pandas as pd
import numpy as np
import requests

# import csv from Hymnary
# the url uses advanced search to filter for multiple things outlined in the params
base_url = "https://hymnary.org/search"
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
url = f"{base_url}?{urlencode(params)}"

hymns = pd.read_csv(url)
texts = pd.read_csv(texts_url)
hymns = hymns.merge(texts[['textAuthNumber', 'yearsWrote']], on='textAuthNumber', how='left')

hymns['popularity'] = (100 * hymns['totalInstances'] / hymns['totalInstances'].max()).astype(int)

class ScriptureHTMLParser(HTMLParser):
    #Set up parser
    def __init__(self):
        super().__init__()
        self.in_ref = False
        self.references = []

    #Inside scripture div
    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "scripture_reference") in attrs:
            self.in_ref = True

    #Outside scripture div
    def handle_endtag(self, tag):
        if tag == "div" and self.in_ref:
            self.in_ref = False

    #Append references to scripture
    def handle_data(self, data):
        if self.in_ref:
            ref = data.strip()
            if ref:
                self.references.append(ref)

def scrape_scripture_references(text_auth_number):
    url = f"https://hymnary.org/text/{text_auth_number}#text-scripture"
    try:
        with urlopen(url) as response:
            html = response.read().decode("utf-8")
        parser = ScriptureHTMLParser()
        parser.feed(html)
        return parser.references if parser.references else None
    except Exception:
        print(f"Scrape failed for {text_auth_number}")
        return None

def get_text(textAuthNumber):
    print(f"Downloading text for {textAuthNumber}...")
    res = requests.get(f"https://hymnary.org/api/fulltext/{textAuthNumber}")

    text = res.json()[0]["text"]
    text = text.replace("\r\n", "\n")
    text = text.replace("\n\n", "\n")

    return text.strip()

hymns['scriptureReferences'] = hymns['textAuthNumber'].apply(scrape_scripture_references)
hymns['text'] = hymns['textAuthNumber'].apply(get_text)

hymns.replace({np.nan: None}, inplace=True)
hymns = hymns[['textAuthNumber', 'displayTitle', 'authors', 'text', 'popularity', 'yearsWrote','scriptureReferences']]

hymns = hymns.rename(columns={
    'textAuthNumber': 'titleId',
    'displayTitle': 'title',
    'yearsWrote': 'publicationYear',
    'scriptureReferences': 'scriptureRefs',
})

# export to json
hymns.to_json("hymns.json", orient="records", indent=2)
