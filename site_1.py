import requests
from bs4 import BeautifulSoup
import os

def get_ads_1(url_bailleur):
# En-têtes pour simuler un navigateur et éviter les blocages
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
# Faire une requête GET pour récupérer le contenu de la page
    response = requests.get(url_bailleur , headers=headers)
# Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialiser les listes pour les types de logements
    maisons_pavillons = []
    appartements = []

    # Afficher le contenu brut de la page
    # print("Contenu brut de la page HTML :")
    # print(soup)

    # Afficher des parties spécifiques du contenu
    print("\néléments trouvés :")
    # Trouver les éléments d'annonces (par exemple, 'div' avec la classe 'views-row')
    ads = soup.find_all('div', class_='views-row')
    for ad in ads:
        title = ad.find('div', class_='field--name-field-titre-de-l-annonce').text.strip() if ad.find('div', class_='field--name-field-titre-de-l-annonce') else 'Titre non disponible'
        location = ad.find('div', class_='localisation').text.strip() if ad.find('div', class_='localisation') else 'Localisation non disponible'
        price = [li.text.strip() for li in ad.find_all('li') if 'Prix de vente' in li.text]
        attribs = ad.find('ul', class_='attributs line_ul')
        if attribs:
            first_li = attribs.find('li')
            ad_type = first_li.text.strip() if first_li else 'Type non disponible'
        else:
            ad_type = 'Type non disponible'

        # Trier les annonces en fonction du type de logement
        if "maison" in ad_type.lower() or "pavillon" in ad_type.lower():
            maisons_pavillons.append((title, location, price, ad_type))
        else:
            appartements.append((title, location, price, ad_type))
    
    # Afficher les résultats triés
    global_compteur = 1

    # Afficher les maisons et pavillons en premier
    print("\nMaisons et Pavillons",url_bailleur, ":")
    for title, location, price, ad_type in maisons_pavillons:
        print(f'Offre {global_compteur}:')
        print(f"\nTitre : {title}")
        print(f"Localisation : {location}")
        print(f"Prix : {', '.join(price)}")
        print(f"Type : {ad_type}")
        global_compteur += 1
"""
    # Ensuite, afficher les appartements
    print("\nAppartements :")
    for title, location, price, ad_type in appartements:
        print(f"\nTitre : {title}")
        print(f"Localisation : {location}")
        print(f"Prix : {', '.join(price)}")
        print(f"Type : {ad_type}")
"""

# Set variables:
##  URL de la page d'annonces
url_bailleur_1  = os.getenv('URL_BAILLEUR_1')

# Si ce fichier est exécuté directement, la fonction suivante sera appelée

if __name__ == "__main__":
    url_bailleur_1 = os.getenv('URL_BAILLEUR_1')
    get_ads_1(url_bailleur_1)