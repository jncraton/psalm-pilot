import os
import json
import pytest
from playwright.sync_api import Page, Locator, expect
from pathlib import Path


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

def test_search_row(main_page: Page, hymn_data: list):
    # Grab the first element and its components to search with
    hymn = hymn_data[0]

    first_title = hymn["title"]
    first_year = hymn['publicationYear']
    first_author = hymn["authors"]
    first_popularity = f"{hymn['popularity']}%"

    # Verify title search works
    main_page.locator("#search").type(first_title)
    expect(main_page.locator("td").get_by_text(first_title).first).to_be_visible()
    expect(main_page.locator("td").get_by_text(hymn_data[1]['title'])).not_to_be_visible()
    main_page.locator("#search").clear()

    # Verify year search works
    main_page.locator("#search").type(first_year)
    expect(main_page.locator("td").get_by_text(first_year).first).to_be_visible()
    main_page.locator("#search").clear()

    # Verify author search works
    main_page.locator("#search").type(first_author)
    expect(main_page.locator("td").get_by_text(first_author).first).to_be_visible()
    main_page.locator("#search").clear()

    # Verify popularity search works
    main_page.locator("#search").type(first_popularity)
    expect(main_page.locator("td").get_by_text(first_popularity).first).to_be_visible()
    main_page.locator("#search").clear()

    # Verify random letters show no results
    main_page.locator("#search").type("asfafaefdawda")
    expect(main_page.locator("td:visible").get_by_text("asfafaef").first).not_to_be_visible()
    main_page.locator("#search").clear()


def test_song_years(main_page: Page, hymn_data: list):
    # Grab hymn publication year source data
    hymn_years = [hymn['publicationYear'] or '' for hymn in hymn_data]

    # Grab the hymn publication year column cells
    hymn_year_cells = get_column_cells(main_page, 'Publication Year')

    # Verify the data matches
    expect(hymn_year_cells).to_have_text(hymn_years)


def test_song_lyrics(main_page:Page, hymn_data: list):
    for hymn in hymn_data:
        # Grab the title source data
        hymn_title_id = hymn['titleId']

        # Grab hymn lyrics source data
        hymn_lyrics = hymn['text']

        # Go to next page 
        main_page.goto(Path(f"hymns/{hymn_title_id}.html").resolve().as_uri())
        
        # Confirm the hymn lyrics on the new page
        expect(main_page.locator("p")).to_contain_text(hymn_lyrics)


