from playwright.sync_api import Page, expect
from pathlib import Path
from typing import Callable
import pytest
import re


def check_directory_fields(page: Page, hymn: dict):
    for key in ['year', 'authors', 'popularity']:
        # Verify directory data matches
        expect(page.locator('dl')).to_contain_text(str(hymn[key]))


def check_lyrics(page: Page, hymn: dict):
    # Confirm the hymn lyrics on current page
    expect(page.locator("blockquote")).to_contain_text(hymn['text'])


def check_hymn_link(page: Page, hymn: dict):
    # Confirm 200 status on link click
    with page.expect_response(re.compile(r"hymnary.org")) as response_info:
        page.get_by_text("hymnary.org").click()
    assert response_info.value.status == 200


@pytest.mark.parametrize("check", [
    check_directory_fields,
    check_lyrics,
    check_hymn_link,
])
def test_hymn_pages(page: Page, hymn_data: list, check: Callable[Page, dict]):
    """Loops through the first two and last two hymn pages to verify things on the page"""
    for hymn in hymn_data[:2] + hymn_data[-2:]:
        page.goto(Path(f"hymns/{hymn['titleId']}.html").resolve().as_uri())

        check(page, hymn)
