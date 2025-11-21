from playwright.sync_api import Page, expect
from pathlib import Path
import re


def test_song_lyrics(page: Page, hymn_data: list):
    for hymn in hymn_data:
        # Grab the title source data
        hymn_title_id = hymn['titleId']

        # Grab hymn lyrics source data
        hymn_lyrics = hymn['text']

        if hymn_lyrics:
            # Go to next page 
            page.goto(Path(f"www/hymns/{hymn_title_id}.html").resolve().as_uri())
            
            # Confirm the hymn lyrics on the new page
            expect(page.locator("blockquote")).to_contain_text(hymn_lyrics)

def test_hymn_link(page: Page, hymn_data: list):
    for hymn in hymn_data[:2] + hymn_data[-2:]:
        page.goto(Path(f"www/hymns/{hymn['titleId']}.html").resolve().as_uri())

        # Confirm 200 status on link click
        with page.expect_response(re.compile(r"hymnary.org")) as response_info:
            page.get_by_text("hymnary.org").click()
        assert response_info.value.status == 200
