import requests
from bs4 import BeautifulSoup

# En-têtes par défaut pour simuler une requête provenant d'un navigateur
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}
#  Fetch the content of a web page and parse it using BeautifulSoup.

def fetch_and_parse(url, headers=DEFAULT_HEADERS):

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        response.raise_for_status()