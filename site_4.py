import requests
from bs4 import BeautifulSoup
import sys
import json

def get_ads_4(url_bailleur):
    # URL de base pour les détails des logements, dérivé de url_bailleur
    base_detail_url = url_bailleur.replace('rechercher?distance=0km&place=%C3%8Ele-de-France&place=%C3%8ELE-DE-FRANCE%3AIDF&tab=PURCHASE&type=Maison', '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    # Faire une requête GET pour récupérer le contenu de la page
    response = requests.get(url_bailleur, headers=headers)
    # Initialisation de BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Localiser le script avec l'ID `__NEXT_DATA__`
    script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
    
    json_data = json.loads(script_tag.string)
        
        # Accéder aux offres dans le JSON
    logements = json_data['props']['pageProps']['defaultSearchResponse']['hits']['hits']
    
    print("\n################# Site 4" ,base_detail_url, "#" * 50)
    print("\nMaisons et Pavillons",url_bailleur, ":")
    print('#' * 100)

    # Extraire les informations pour chaque offre
    for logement in logements:
        # Extraire les informations spécifiques
        title = logement['_source'].get('title')
        ville = logement['_source']['data'].get('ville',{}).get('value')
        code_postal  = logement['_source']['data'].get('code_postal',{}).get('value')
        location = ville + ' ' + code_postal
        price = logement['_source'].get('transaction', {}).get('price')
        product_type = logement['_source'].get('productType', {}).get('description')
        reference   =   logement['_source'].get('reference')
        link    =   f"{base_detail_url}offre/{title.replace(' ', '%20')}/{reference}"
        surface = logement['_source']['data'].get('surface_habitable', {}).get('value')
        surface_unit = logement['_source']['data'].get('surface_habitable', {}).get('unit')
        # description = offer['_source'].get('description', 'N/A')
        bedrooms = logement['_source']['data'].get('nombre_de_chambres', {}).get('value')
        rooms = logement['_source'].get('data', {}).get('nb_pieces_logement', {}).get('value')
        contact_name = logement['_source']['data'].get('contact_a_afficher', {}).get('value')
        contact_phone = logement['_source']['data'].get('telephone_mobile_a_afficher', {}).get('value')

        # Afficher les informations
        print(f"Titre : {title}")
        print(f"Localisation : {location}")
        print(f"Prix : {price} €")
        print(f"Type : {product_type}")
        print(f"Surface : {surface} {surface_unit}")
        # print(f"Description : {description}")
        print(f"Chambres : {bedrooms}")
        print(f"Pièces : {rooms}")
        print(f"Contact : {contact_name}")
        print(f"Téléphone : {contact_phone}")
        print(f"Lien : {link}")
        print("-" * 50)

    maisons_pavillons = []
    appartements = []

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_4(url)