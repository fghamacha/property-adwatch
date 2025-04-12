# import librairies
import requests
from bs4 import BeautifulSoup
import sys
import yaml
# import my functions
from save_to_yaml import save_to_yaml
from functions.scraping import fetch_and_parse



def get_ads_5(url):
  #   Initier les variables : 
    base_detail_url = url.replace('/fr/recherche?page=', '')
    compteur_maison = 1
    compteur_appartement = 1
    maisons = {base_detail_url: {}}
    appartements = {base_detail_url: {}}

    # Utiliser la fonction fetch_and_parse pour obtenir le contenu HTML
    soup = fetch_and_parse(url)
    # récupérer la balise de toutes les annonces
    ads = soup.select('li.property')

    # Trouver toutes les annonces
    for ad in ads:
        try:
            # Récupérer les informations nécessaires
            title = ad.select_one('div.picture a')['title'].strip()
            price = ad.select_one('span.price').text.strip().replace('\u202f', ' ')  # Remove thin space
            location = ad.select_one('div.content h3').text.strip()
            ########################################################
            # Get rooms, area, and bedrooms
            ########################################################
            details = ad.select('div.infos ul li')
            rooms = None
            area = None
            bedrooms = None
            for detail in details:
                if 'rooms' in detail.get('class', []):
                    rooms = detail.get('data-details', '').strip()
                elif 'area' in detail.get('class', []):
                    area = detail.text.strip()
                elif 'bedrooms' in detail.get('class', []):
                    bedrooms = detail.text.strip()
            ########################################################
                link = ad.select_one('div.picture a')['href']
            full_link = f"{base_detail_url.rstrip('/')}{link}"
            # Déterminer si c'est un appartement ou une maison
            type_ad = ad.select_one('p.type').text.strip().lower()
        except (AttributeError, KeyError) as e:
        # Ignorer les annonces mal formées
            print("Une annonce n'a pas pu être parsée correctement:", e)
            continue

        # Trier les annonces en fonction du type de logement
        if "appartement" in type_ad :
            logement  =   {
                'id': compteur_appartement,
                'Titre': title,
                'Prix': price,
                'Localisation': location,
                'Type': 'appartement',
                'Pièces': rooms,
                'Lien': full_link               
            }
            appartements[base_detail_url][f"logement {compteur_appartement}"] = logement
            compteur_appartement +=1
        else:
            logement  =   {
                'id': compteur_maison,
                'Titre': title,
                'Prix': price,
                'Localisation': location,
                'Type': 'maison',
                'Pièces': rooms,
                'Lien': full_link                   
            }
            maisons[base_detail_url][f"logement {compteur_maison}"] = logement
            compteur_maison +=1


    # Enregistrer les données dans un fichier YAML
    save_to_yaml('maisons.yaml', maisons)
    save_to_yaml('appartements.yaml', appartements) 

if __name__ == "__main__":
    url = sys.argv[1]
    # Récupérer les annonces
    get_ads_5(url) 
