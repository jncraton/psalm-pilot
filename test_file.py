import re
import os
import pytest
from playwright.sync_api import Page, expect

def test_html_file(page: Page):
    path = os.path.abspath('index.html')
    page.goto(f"file://{path}")

    assert page.title() == "Palm Pilot"
