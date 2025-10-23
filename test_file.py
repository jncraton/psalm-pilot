import os
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def main_page(page: Page) -> Page:
    page.goto(f"file://{os.path.abspath('index.html')}")

    return page

def test_html_file(main_page: Page):
    expect(main_page).to_have_title("Psalm Pilot")

def test_table_not_empty(main_page: Page):
    row_locator = main_page.locator("table tbody tr")
    expect(row_locator).not_to_have_count(0)
