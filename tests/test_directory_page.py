import os
import re
from playwright.sync_api import Page, Locator, expect


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


def test_directory_sanity(directory_page: Page):
    row_locator = directory_page.locator("tbody tr")
    expect(row_locator).not_to_have_count(0)


def test_chat(directory_page: Page):
    directory_page.on('dialog', lambda d: d.accept(os.environ["GEMINI_API_KEY"]))

    response = directory_page.evaluate("chat('What is the capital of France?')")
    assert "Paris" in response


def test_song_titles(directory_page: Page, hymn_data: list):
    # Grab hymn title source data
    hymn_titles = [hymn['title'] for hymn in hymn_data]

    # Grab the hymn title column cells
    hymn_title_cells = get_column_cells(directory_page, 'Title')

    # Verify the data matches
    expect(hymn_title_cells).to_have_text(hymn_titles)


def test_song_popularity(directory_page: Page, hymn_data: list):
    # Grab hymn popularity source data
    hymn_popularity = [f"{hymn['popularity']}%" for hymn in hymn_data]

    # Grab the hymn popularity column cells
    hymn_popularity_cells = get_column_cells(directory_page, 'Popularity')

    # Verify the data matches
    expect(hymn_popularity_cells).to_have_text(hymn_popularity)


def test_song_authors(directory_page: Page, hymn_data: list):
    # Grab hymn authors source data, converting None to empty string
    hymn_authors = [hymn['authors'] or '' for hymn in hymn_data]

    # Grab the hymn authors column cells
    hymn_author_cells = get_column_cells(directory_page, 'Author')

    # Verify the data matches
    expect(hymn_author_cells).to_have_text(hymn_authors)


def test_song_years(directory_page: Page, hymn_data: list):
    # Grab hymn publication year source data
    hymn_years = [hymn['year'] or '' for hymn in hymn_data]

    # Grab the hymn publication year column cells
    hymn_year_cells = get_column_cells(directory_page, 'Year')

    # Verify the data matches
    expect(hymn_year_cells).to_have_text(hymn_years)


def test_song_search(directory_page: Page, hymn_data: list):
    hymn = hymn_data[0]

    search_bar = directory_page.locator('#search')
    cells = directory_page.locator('td')
    
    def get_non_matching_hymn(query: str) -> Locator:
        """Finds a hymn instance that should not show up with given query"""

        for hymn in hymn_data[1:]:
            if not any(query in str(field) or query == str(field) for field in hymn.values()):
                return cells.get_by_text(hymn['title'])
        
        raise Exception(f"No non-matching hymn was found for query: {query}")

    # Query, verify, and clear for each field
    for key in ['title', 'year', 'authors', 'popularity']:
        query = str(hymn[key])

        search_bar.type(query)
        expect(cells.get_by_text(hymn['title'])).to_be_visible()
        expect(get_non_matching_hymn(query)).not_to_be_visible()
        search_bar.clear()

    # Verify random letters show no results
    search_bar.type('asfafaefdawda')
    for i in range(cells.count()):
        expect(cells.nth(i)).not_to_be_visible()

    # Verify no letters shows all results
    search_bar.clear()
    for i in range(cells.count()):
        expect(cells.nth(i)).to_be_visible()
        
        
def test_navigate_to_hymn_via_title_link(directory_page: Page, hymn_data: list):
    for hymn in hymn_data:
        hymn_title = hymn['title']
        hymn_title_id = hymn['titleId']

        # Click the link to go to the hymn page
        directory_page.get_by_role("link", name=hymn_title, exact=True).click()

        # Confirm the URL is correct
        expect(directory_page).to_have_url(
            re.compile(f".*/hymns/{hymn_title_id}.html"))

        # Go back to the directory page
        directory_page.go_back()