from playwright.sync_api import Page, expect
from pathlib import Path
from typing import Callable
import pytest
import re


def test_navigate_to_hymn_pages(directory_page: Page, hymn_data: list[dict[str, any]]):
    for hymn in hymn_data[:2] + hymn_data[-2:]:
        # Click the link to go to the hymn page
        directory_page.get_by_role("link", name=hymn['title'], exact=True).click()

        # Verify URL and title on page
        expect(directory_page).to_have_url(re.compile(f".*/hymns/{hymn['titleId']}.html"))
        expect(directory_page.locator("h2")).to_have_text(hymn['title'])

        # Go back to the directory page
        directory_page.go_back()


def check_directory_fields(page: Page, hymn: dict):
    for key in ['year', 'authors', 'popularity']:
        # Verify directory data matches
        expect(page.get_by_text(key.capitalize()).locator("+ dd")).to_contain_text(str(hymn[key]))


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
        page.goto(Path(f"www/hymns/{hymn['titleId']}.html").resolve().as_uri())

        check(page, hymn)
