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


def test_song_authors(main_page: Page, hymn_data: list):
    # Grab hymn authors source data
    hymn_authors = [hymn['authors'] for hymn in hymn_data]

    # Grab the hymn authors column cells
    hymn_author_cells = main_page.locator("td:nth-child(2)")

    # Verify the cells and data are of same length
    expect(hymn_author_cells).to_have_count(len(hymn_authors))

    # Verify the data matches
    for hymn_authors_cell, hymn_author in zip(hymn_author_cells.all(), hymn_authors):
        
        if hymn_author is not None:
            expect(hymn_authors_cell).to_have_text(hymn_author)
        else:
            expect(hymn_authors_cell).to_be_empty()