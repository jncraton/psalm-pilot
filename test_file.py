import os
from playwright.sync_api import Page, expect

def test_html_file(page: Page):
    path = os.path.abspath('index.html')
    page.goto(f"file://{path}")

    expect(page).to_have_title("Psalm Pilot")

def test_table_not_empty(page: Page):
    path = os.path.abspath('index.html')
    page.goto(f"file://{path}")

    row_locator = page.locator("table tbody tr")
    # row_count=row_locator.count()
    # print({row_count})
    expect(row_locator).not_to_have_count(0)
