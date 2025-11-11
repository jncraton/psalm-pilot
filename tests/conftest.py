import json
import pytest
from playwright.sync_api import Page
from pathlib import Path

@pytest.fixture
def main_page(page: Page) -> Page:
    """Goes to the main page of app and returns Page object in that state."""
    page.goto(Path('index.html').resolve().as_uri())

    return page


@pytest.fixture(scope='session')
def hymn_data() -> list:
    """Grabs the hymns source data for verification comparison."""
    with open('data/hymns.json', 'r') as file:
        data = json.load(file)
    
    return data