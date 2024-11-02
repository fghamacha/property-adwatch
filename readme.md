
How to get the content of a web site 
we use the python function requests.get(URL) from the librery  requests

```py
# Import requests librery
import requests
# Define a site to scrape 
url_bailleur= 'https://<my_site_to_scrap>.com/<context_to_my_ads>''
#  get request to reponse
response = requests.get(url_bailleur)
# Get the content of the site 
response.text
# To get the status code : 
response.status_code
# Get the encoding 
response.encoding   
```

We use Python's BeautifulSoup library to parse and manipulate HTML content returned by the website,

```py
from bs4 import BeautifulSoup
import requests
# Fetch the page content
response = requests.get(url_bailleur)
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')
```

Webography

- [Request Librery](https://requests.readthedocs.io/en/latest/)