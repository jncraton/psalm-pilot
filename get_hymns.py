import pandas as pd

# import csv from Hymnary and retrieve first 100 hymn titles
# the url is using advanced search to filter for public domain, English langauge, text-only files, and Church of God denomination
url = "https://hymnary.org/texts?qu=textLanguages%3Aenglish%20denominations%3Achurch%20of%20god%20media%3Atext%20textClassification%3Atextispublicdomain%20tuneClassification%3Atuneispublicdomain%20in%3Atexts&export=csv&limit=384"
hymns = pd.read_csv(url)
hymn_titles = hymns['displayTitle'].head(100)

# export as .json
hymn_titles.to_json("hymns.json", compression='infer', index=False)