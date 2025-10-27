import os
import json
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def main_page(page: Page) -> Page:
    """Goes to the main page of app and returns Page object in that state."""
    page.goto(f"file://{os.path.abspath('index.html')}")

    return page


@pytest.fixture
def hymn_data() -> list:
    """Grabs the hymns source data for verification comparison."""
    with open('data/hymns.json', 'r') as file:
        data = json.load(file)
    
    return data


def test_html_file(main_page: Page):
    expect(main_page).to_have_title("Psalm Pilot")


def test_table_not_empty(main_page: Page):
    row_locator = main_page.locator("tbody tr")
    expect(row_locator).not_to_have_count(0)


def test_browse_hymns(main_page: Page, hymn_data: list):
    # Grab hymn title source data
    hymn_titles = [hymn['title'] for hymn in hymn_data]

    # Grab the hymn title column cells
    hymn_title_cells = main_page.locator("td:nth-child(1)")

    # Verify the data matches
    expect(hymn_title_cells).to_have_text(hymn_titles)