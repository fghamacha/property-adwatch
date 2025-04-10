import requests
from bs4 import BeautifulSoup
import yaml
import sys
from save_to_yaml import save_to_yaml
from scripts.extract_number_from_type import extract_number_from_type
from functions.scraping import fetch_and_parse

def get_ads_1(url_bailleur):
    # URL de base pour les détails des logements, dérivé de url_bailleur
    base_detail_url = url_bailleur.replace('/biens?type_de_bien=hlm&louer_ou_acheter=acheter&', '')
    
    # Utiliser la fonction fetch_and_parse pour obtenir le contenu HTML
    soup = fetch_and_parse(url)
    
    # Initialiser les listes pour les types de logements
    maisons = {
        base_detail_url: {}
    }
    appartements = {
        base_detail_url: {}
    }

    # Trouver les éléments d'annonces (par exemple, 'div' avec la classe 'views-row')
    ads = soup.find_all('div', class_='views-row')
    compteur_maison = 1
    compteur_appartement =1

    for ad in ads:
        title = ad.find('div', class_='field--name-field-titre-de-l-annonce').text.strip() if ad.find('div', class_='field--name-field-titre-de-l-annonce') else 'Titre non disponible'
        location = ad.find('div', class_='localisation').text.strip() if ad.find('div', class_='localisation') else 'Localisation non disponible'
        price = [li.text.strip() for li in ad.find_all('li') if 'Prix de vente' in li.text]
        attribs = ad.find('ul', class_='attributs line_ul')
         # Récupérer le lien de l'annonce
        link_tag = ad.find('a', class_='orange ft-14 parking-teaser_more underlined')
        link = base_detail_url + link_tag['href'] if link_tag else 'Lien non disponible'

        if attribs:
            first_li = attribs.find('li')
            ad_type = first_li.text.strip() if first_li else 'Type non disponible'
        else:
            ad_type = 'Type non disponible'
        rooms = extract_number_from_type(ad_type)
        # Trier les annonces en fonction du type de logement
        if "maison" in ad_type.lower() or "pavillon" in ad_type.lower():
            logement  =   {
                'id': compteur_maison,
                'Titre': title,
                'Prix': ', '.join(price),
                'Localisation': location,
                'Type': ad_type,
                'Pièces': rooms,
                'Lien': link
            }
            maisons[base_detail_url][f"logement {compteur_maison}"] = logement
            compteur_maison +=1
        else:
            logement  =   {
                'id': compteur_appartement,
                'Titre': title,
                'Prix': ', '.join(price),
                'Localisation': location,
                'Type': ad_type,
                'Pièces': rooms,
                'Lien': link
            }
            appartements[base_detail_url][f"logement {compteur_appartement}"] = logement
            compteur_appartement +=1


    # Enregistrer les données dans un fichier YAML
    save_to_yaml('maisons.yaml', maisons)
    save_to_yaml('appartements.yaml', appartements)     


# Si ce fichier est exécuté directement, la fonction suivante sera appelée

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_1(url)