import requests
from bs4 import BeautifulSoup

def fetch_page(url, headers=None):
    """Fetch the content of a web page."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_html(html_content):
    """Parse HTML content using BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')
