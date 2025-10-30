import os
import json
import pytest
from playwright.sync_api import Page, Locator, expect

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


def get_column_index(page: Page, column_name: str) -> int:
    """Finds the index of a column by the name of it"""
    # Grab header cells
    header_cells = page.locator("th")

    # Find the the matching column name
    for i in range(header_cells.count()):
        if column_name in header_cells.nth(i).inner_html():
            return i + 1

    # If not found return error
    raise ValueError(f"Column name {column_name} not found")


def get_column_cells(page: Page, column_name: str) -> Locator:
    """Grabs the cells of a column by the name of it"""
    # Find the column index
    column_index = get_column_index(page, column_name)

    # Return the locator of that index
    return page.locator(f"td:nth-child({column_index})")


def test_html_file(main_page: Page):
    expect(main_page).to_have_title("Psalm Pilot")


def test_table_not_empty(main_page: Page):
    row_locator = main_page.locator("tbody tr")
    expect(row_locator).not_to_have_count(0)

def test_chat(main_page: Page):
    main_page.get_by_text("AI Settings").click()
    main_page.get_by_label("Gemini Key").fill(os.environ["GEMINI_KEY"])
    main_page.get_by_text("Save Key").click()
    expect(main_page.get_by_text("Gemini Ready")).to_be_visible()

def test_song_titles(main_page: Page, hymn_data: list):
    # Grab hymn title source data
    hymn_titles = [hymn['title'] for hymn in hymn_data]

    # Grab the hymn title column cells
    hymn_title_cells = get_column_cells(main_page, 'Title')

    # Verify the data matches
    expect(hymn_title_cells).to_have_text(hymn_titles)


def test_song_popularity(main_page: Page, hymn_data: list):
    # Grab hymn popularity source data
    hymn_popularity = [f"{hymn['popularity']}%" for hymn in hymn_data]

    # Grab the hymn popularity column cells
    hymn_popularity_cells = get_column_cells(main_page, 'Popularity')

    # Verify the data matches
    expect(hymn_popularity_cells).to_have_text(hymn_popularity)


def test_song_authors(main_page: Page, hymn_data: list):
    # Grab hymn authors source data, converting None to empty string
    hymn_authors = [hymn['authors'] or '' for hymn in hymn_data]

    # Grab the hymn authors column cells
    hymn_author_cells = get_column_cells(main_page, 'Author')

    # Verify the data matches
    expect(hymn_author_cells).to_have_text(hymn_authors)


def test_song_years(main_page: Page, hymn_data: list):
    # Grab hymn publication year source data
    hymn_years = [hymn['publicationYear'] or '' for hymn in hymn_data]

    # Grab the hymn publication year column cells
    hymn_year_cells = get_column_cells(main_page, 'Publication Year')

    # Verify the data matches
    expect(hymn_year_cells).to_have_text(hymn_years)