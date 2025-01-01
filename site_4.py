import requests
from bs4 import BeautifulSoup
import sys
import json
from save_to_yaml import save_to_yaml
import yaml


def get_ads_4(url_bailleur):
    # URL de base pour les détails des logements, dérivé de url_bailleur
    base_detail_url = url_bailleur.replace('/rechercher?distance=0km&place=%C3%8Ele-de-France&place=%C3%8ELE-DE-FRANCE%3AIDF&tab=PURCHASE&type=Maison', '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    # Faire une requête GET pour récupérer le contenu de la page
    response = requests.get(url_bailleur, headers=headers)
    # Initialisation de BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Initialiser les listes pour les types de logements
    compteur_maison = 1
    compteur_appartement =1
    maisons = {
        base_detail_url: {}
    }
    # Localiser le script avec l'ID `__NEXT_DATA__`
    script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
    
    json_data = json.loads(script_tag.string)
        
        # Accéder aux offres dans le JSON
    ads = json_data['props']['pageProps']['defaultSearchResponse']['hits']['hits']
    
    # print("\n################# Site 4" ,base_detail_url, "#" * 50)
    # print("Maisons et Pavillons",url_bailleur)
    # print('#' * 100)

    # Extraire les informations pour chaque offre
    for ad in ads:
        # Extraire les informations spécifiques
        title = ad['_source'].get('title')
        ville = ad['_source']['data'].get('ville',{}).get('value')
        code_postal  = ad['_source']['data'].get('code_postal',{}).get('value')
        location = ville + ' ' + code_postal
        price = ad['_source'].get('transaction', {}).get('price')
        product_type = ad['_source'].get('productType', {}).get('description')
        reference   =   ad['_source'].get('reference')
        link    =   f"{base_detail_url}offre/{title.replace(' ', '%20')}/{reference}"
        surface = ad['_source']['data'].get('surface_habitable', {}).get('value')
        surface_unit = ad['_source']['data'].get('surface_habitable', {}).get('unit')
        # description = offer['_source'].get('description', 'N/A')
        bedrooms = ad['_source']['data'].get('nombre_de_chambres', {}).get('value')
        rooms = ad['_source'].get('data', {}).get('nb_pieces_logement', {}).get('value')
        contact_name = ad['_source']['data'].get('contact_a_afficher', {}).get('value')
        contact_phone = ad['_source']['data'].get('telephone_mobile_a_afficher', {}).get('value')
        logement  =    {
            'id': compteur_maison,
            'Titre': title,
            'Prix': price,
            'Localisation': location,
            'Type': product_type,
            'Surface': surface,
            'Chambres': bedrooms,
            'Pièces': rooms,
            'Contact': contact_name,
            'Téléphone': contact_phone,
            'Lien': link
        }
        maisons[base_detail_url][f"logement {compteur_maison}"] = logement
        compteur_maison +=1


    # Enregistrer les données dans un fichier YAML
    # print(logements)
    save_to_yaml('maisons.yaml', maisons)

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_4(url)