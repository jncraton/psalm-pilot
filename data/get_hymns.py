from urllib.parse import urlencode
from urllib.request import urlopen
from html.parser import HTMLParser
import pandas as pd
import numpy as np
import re
from tqdm import tqdm

tqdm.pandas()

# import csv from Hymnary
# the url uses advanced search to filter for multiple things outlined in the params
base_url = "https://hymnary.org/search"
texts_url = "https://hymnary.org/files/hymnary/other/texts.csv"

params = {
    "qu": {
        "textLanguages": "english",
        "hymnalNumber": "CCLI",
        "in": "instances",
    },
    "sort": "displayTitle",
    "export": "csv",
    "limit": 10000
}

params["qu"] = " ".join([f"{k}:{v}" for k, v in params["qu"].items()])
url = f"{base_url}?{urlencode(params)}"

instances = pd.read_csv(url)
instances["ccliPopularity"] = 101 - instances["number"]

ccli_hymns = ( 
    instances.groupby("textAuthNumber")
    .agg(
        {
            "ccliPopularity": "sum",
            "displayTitle": "first",
            "authors": "first",
        }
    )
    .sort_values(by=["ccliPopularity"], ascending=False)
    .reset_index()
)

ccli_hymns["ccliPopularity"] = (100 * ccli_hymns["ccliPopularity"] / ccli_hymns["ccliPopularity"].max()).astype(int)

params = {
    "qu": {
        "textLanguages": "english",
        "media": "text",
        "in": "texts",
    },
    "sort": "totalInstances",
    "export": "csv",
    "limit": 300
}

params["qu"] = " ".join([f"{k}:{v}" for k, v in params["qu"].items()])
url = f"{base_url}?{urlencode(params)}"

hymns = pd.read_csv(url)
hymns['hymnalPopularity'] = (100 * hymns['totalInstances'] / hymns['totalInstances'].max()).astype(int)

hymns = pd.concat([hymns, ccli_hymns])

hymns['popularity'] = hymns[['ccliPopularity', 'hymnalPopularity']].max(axis=1).astype(int)

hymns = hymns.groupby('textAuthNumber').agg({
    'popularity': 'max',
    "displayTitle": "first",
    "authors": "first",
}).sort_values(by=["popularity"], ascending=False).reset_index()

texts = pd.read_csv(texts_url)
hymns = hymns.merge(texts[['textAuthNumber', 'yearsWrote', 'firstLine', 'refrainFirstLine']], on='textAuthNumber', how='left')

class ScriptureHTMLParser(HTMLParser):
    #Set up parser
    def __init__(self):
        super().__init__()
        self.in_ref = False
        self.references = []
        self.in_text = False
        self.lyrics = ""

    #Inside scripture div
    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "scripture_reference") in attrs:
            self.in_ref = True
        if tag == "div" and ("property", "text") in attrs and not self.lyrics:
            self.in_text = True
        if tag == "p" and self.in_text:
            self.lyrics += "\n\n"
        if tag == "br" and self.in_text:
            self.lyrics += "\n"

    #Outside scripture div
    def handle_endtag(self, tag):
        if tag == "div":
            self.in_ref = False
            self.in_text = False

    #Append references to scripture
    def handle_data(self, data):
        if self.in_ref:
            ref = data.strip()
            if ref:
                self.references.append(ref)

        if self.in_text:
            dataNoNewlines = re.sub("[\r\n]", "", data)
            dataNormalized = re.sub("\t", " ", dataNoNewlines).strip()
            self.lyrics = re.sub("\n\n\n+", "\n\n", self.lyrics + dataNormalized)

def scrape(text_auth_number):
    url = f"https://hymnary.org/text/{text_auth_number}#text-scripture"
    try:
        with urlopen(url) as response:
            html = response.read().decode("utf-8")
        parser = ScriptureHTMLParser()
        parser.feed(html)
        return pd.Series({
                    'text': parser.lyrics.strip() or None,
                    'scriptureReferences': parser.references or None,
                })
    except Exception:
        raise Exception(f"Scrape failed for {text_auth_number}")

hymns[['text', 'scriptureReferences']] = hymns['textAuthNumber'].progress_apply(scrape)

def combine_refs(refs):
    # Removes multiple instances of Books for Chapters
    if not refs:
        return refs

    combined = {}
    for ref in refs:
        # Find the last space before the chapter:verse part
        # Therefore "1 Corinthians 2:39" will be separated into "1 Conrinthians""2:39"
        last_space = ref.rfind(" ")
        if last_space != -1:
            book = ref[:last_space]
            chap = ref[last_space + 1:]
            combined.setdefault(book, []).append(chap)
        else:
            # No spaces found (very rare)
            combined.setdefault("", []).append(ref)

     # Join references and strip any trailing spaces
    return [f"{book} {'; '.join(ref_list)}".strip() for book, ref_list in combined.items()]


# Apply combination
hymns['scriptureReferences'] = hymns['scriptureReferences'].apply(combine_refs)

hymns = hymns[['textAuthNumber', 'displayTitle', 'authors', 'text', 'firstLine', 'refrainFirstLine', 'popularity', 'yearsWrote','scriptureReferences']]
hymns.replace({np.nan: None}, inplace=True)

hymns = hymns.rename(columns={
    'textAuthNumber': 'titleId',
    'displayTitle': 'title',
    'yearsWrote': 'year',
    'scriptureReferences': 'scriptureRefs',
})

# export to json
hymns.to_json("hymns.json", orient="records", indent=2)
