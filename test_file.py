import os
import json
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
    # Grab the hymn source data
    with open('data/hymns.json', 'r') as file:
        hymns = json.load(file)

    hymn_titles = [hymn['title'] for hymn in hymns]

    # Grab the hymn title column cells
    hymn_title_cells = main_page.locator("tr td:nth-child(1)")

    # Verify the data matches
    expect(hymn_title_cells).to_have_text(hymn_titles)