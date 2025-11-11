import os
import json
import pytest
from playwright.sync_api import Page

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