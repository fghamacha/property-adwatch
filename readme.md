# Property Ad Watch

Property Ad Watch is a Python-based web scraping project that collects property ads from multiple websites. The project centralizes the collected data in a shared YAML file for easy analysis and storage.

How to get the content of a web site 
we use the python function requests.get(URL) from the librery  requests

# Features

- Multi-Site Scraping: Extract data from multiple real estate websites.
- Data Aggregation: Append and merge new listings into a shared YAML file.
- Customizable: Easily add new sites by creating new Python scripts.
- Automated Execution: Leverages GitHub Actions for scheduled or manual execution

# Project Structure

```md
property_adwatch/
│
├── .github/
│   └── workflows/
│       └── main.yml   # GitHub Actions workflow to run python scripts and display yaml file
│
├── functions/
|   ├── _init_.py
|   ├── email_utils.py
|   ├── scrapping.py
|   └── scripts.py
|
├── main.py             # main python script to run all specific python scripts
├── site_0.py           # Scraper for site 0
├── site_1.py           # Scraper for site 1
├── site_2.py           # Scraper for site 2
├── site_4.py           # Scraper for site 4
├── site_5.py           # Scraper for site 5
|
├── requirements.txt    # Python dependencies
├── CHANGELOG.md
└── README.md           # Project documentation
```

# How It Works
1. Scrapers: Each scraper script (site_1.py, site_2.py, etc.) scrapes property listings from a specific website, extracting details like title, price, location, features, and a link to the listing.

2. Data Storage: Listings are saved to a shared YAML file (maisons.yaml). The save_to_yaml.py python script ensures that data from different scripts is merged without overwriting existing entries.

3. Execution:

- The main entry point for running all scrapers is main.py.
- GitHub Actions is configured to execute the scripts automatically on:
    - Push to the main branch.
    - Scheduled daily at 7:00 AM UTC.
    - Manual trigger on other branches.

##  Usage

#### Prerequisites
- Python 3.9 or higher
- Install dependencies:

```sh
pip install -r requirements.txt
```
#### Run Locally
To scrape data manually

1. create .env file in the main repository directory with the following values : 

```sh
URL_BAILLEUR_0=""
URL_BAILLEUR_1=""
URL_BAILLEUR_2=""
URL_BAILLEUR_4=""
URL_BAILLEUR_5=""

# URL_BAILLEUR_3="" not working yet
 
EMAIL_SENDER="<username>a@gmail.com"
EMAIL_RECIPIENTS=["username@gmail.com","username@gmail.com"]
EMAIL_PASSWORD="xxxx xxxx xxxx xxxx"
EMAIL_THREAD_ID_MAISONS="<xxxxxxxxxxxxxxxxxx@mx.google.com>"
EMAIL_THREAD_ID_APPARTEMENTS="xxxxxxxxxxxxxx@mx.google.com>"
```

Notes: 
    -   you can get create your gmail app password here https://myaccount.google.com/apppasswords 

2. execute the scraper scripts with the desired URL:

```sh
python <MY_SITE>.py "https://<MY_SITE>"
```

#### Run with GitHub Actions

- Push changes to the main branch to trigger the workflow automatically.
- Use the GitHub Actions interface to trigger workflows manually on other branches.

#### Configuration

###### Environment Variables

- Define environment variables in the GitHub repository settings for dynamic URLs:
- URL_BAILLEUR_0
- URL_BAILLEUR_1
- URL_BAILLEUR_2
- URL_BAILLEUR_4
- URL_BAILLEUR_5

The- URL_BAILLEUR_1 will be injected into the scripts during execution.

# License

 i didn't define any license for this project.

# Play with python

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

- In Python web scraping, the select_one method is used to select the first matching element based on a given CSS selector

```py
from bs4 import BeautifulSoup
import requests
# Fetch the page content
response = requests.get(url_bailleur)
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')
```

# Webography

- [Request Librery](https://requests.readthedocs.io/en/latest/)