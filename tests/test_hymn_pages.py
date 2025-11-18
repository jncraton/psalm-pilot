from playwright.sync_api import Page, expect
from pathlib import Path
import pytest
import re


# @pytest.mark.parametrize("check", [
#     check_directory_fields,
#     check_title,
#     check_lyrics_present,
# ])
# def check_hymn_pages(page: Page, hymn_data: list, check: Callable[Page, dict]):
#     """Loops through the first two and last two hymn pages to verify things on the page"""
#     for hymn in hymn_data[:2] + hymn_data[-2:]:
#         page.goto(Path(f"hymns/{hymn['titleId']}.html").resolve().as_uri())

#         check(page, hymn)


def test_directory_data_on_hymn_page(page: Page, hymn_data: list):
    for hymn in hymn_data[:2] + hymn_data[-2:]:
        page.goto(Path(f"hymns/{hymn['titleId']}.html").resolve().as_uri())

        for key in ['publicationYear', 'authors', 'popularity']:
            # Verify directory data matches
            expect(page.locator('dl')).to_contain_text(str(hymn[key]))


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


def test_hymn_link(page: Page, hymn_data: list):
    for hymn in hymn_data[:2] + hymn_data[-2:]:
        page.goto(Path(f"hymns/{hymn['titleId']}.html").resolve().as_uri())

        # Confirm 200 status on link click
        with page.expect_response(re.compile(r"hymnary.org")) as response_info:
            page.get_by_text("hymnary.org").click()
        assert response_info.value.status == 200
