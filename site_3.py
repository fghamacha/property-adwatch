import requests
from bs4 import BeautifulSoup

def get_ads_3(url):
    # Set up headers to mimic a browser request
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    # Send a request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Unable to access the page (status code {response.status_code})")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

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
    url_site_3 = 'https://www.havitat.fr/trouvez-votre-logement?locations=%C3%8Ele-de-France%2C%C3%8Ele-de-France&type_bien=f-maison'
    get_ads_3(url_site_3)
