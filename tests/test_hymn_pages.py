from playwright.sync_api import Page, expect
from pathlib import Path


def test_song_lyrics(page: Page, hymn_data: list):
    for hymn in hymn_data:
        # Grab the title source data
        hymn_title_id = hymn['titleId']

        # Grab hymn lyrics source data
        hymn_lyrics = hymn['text']

        # Go to next page 
        page.goto(Path(f"hymns/{hymn_title_id}.html").resolve().as_uri())
        
        # Confirm the hymn lyrics on the new page
        expect(page.locator("blockquote")).to_contain_text(hymn_lyrics)