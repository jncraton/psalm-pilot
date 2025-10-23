import os
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def main_page(page: Page) -> Page:
    """Goes to the main page of app and returns Page object in that state."""
    page.goto(f"file://{os.path.abspath('index.html')}")

    return page


def test_html_file(main_page: Page):
    expect(main_page).to_have_title("Psalm Pilot")


def test_table_not_empty(main_page: Page):
    row_locator = main_page.locator("tbody tr")
    expect(row_locator).not_to_have_count(0)


def test_browse_hymns(main_page: Page):
    hymn_title_cells = main_page.locator("tr td:nth-child(1)")

    for i in range(hymn_title_cells.count()):
        expect(hymn_title_cells.nth(i)).not_to_be_empty()