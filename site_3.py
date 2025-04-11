import requests
import sys
from bs4 import BeautifulSoup
from functions.scraping import fetch_and_parse

def get_ads_3(url):

    # Utiliser la fonction fetch_and_parse pour obtenir le contenu HTML
    soup = fetch_and_parse(url)

    # Initialize lists for storing different types of properties
    maisons_pavillons = []
    appartements = []

    # Find all property listings on the page
    listings = soup.find_all('div', class_='views-row')  # Adjust the class name based on actual structure

    for listing in listings:
        # Extract the title of the listing
        title = listing.find('div', class_='field--name-field-titre-de-l-annonce').text.strip() if listing.find('div', class_='field--name-field-titre-de-l-annonce') else 'Titre non disponible'
        
        # Extract the location
        location = listing.find('div', class_='localisation').text.strip() if listing.find('div', class_='localisation') else 'Localisation non disponible'
        
        # Extract the price
        price = listing.find('span', class_='price').text.strip() if listing.find('span', class_='price') else 'Prix non disponible'

        # Extract the link to the detailed page
        link = listing.find('a', href=True)['href'] if listing.find('a', href=True) else 'Lien non disponible'

        # Determine if the listing is for a house, pavilion, or apartment
        if "maison" in title.lower() or "pavillon" in title.lower():
            maisons_pavillons.append((title, location, price, link))
        else:
            appartements.append((title, location, price, link))

    # Display the listings, starting with houses and pavilions
    print("\nMaisons et Pavillons :")
    for title, location, price, link in maisons_pavillons:
        print(f"Titre : {title}")
        print(f"Localisation : {location}")
        print(f"Prix : {price}")
        print(f"Lien : {link}")
        print('-' * 40)

    # Commented out the apartments section
    """
    print("\nAppartements :")
    for title, location, price, link in appartements:
        print(f"Titre : {title}")
        print(f"Localisation : {location}")
        print(f"Prix : {price}")
        print(f"Lien : {link}")
        print('-' * 40)
    """

# Example usage of the function
if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_3(url)
