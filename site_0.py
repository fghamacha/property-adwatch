import requests
from bs4 import BeautifulSoup
import sys
import yaml
from functions.scraping import fetch_and_parse, save_to_yaml

def get_ads_0(url):
    
  #   Initier les variables : 
    base_detail_url = url.replace('/nos-logements-en-vente', '')
    page = 0
    compteur_maison = 1
    compteur_appartement = 1
    maisons = {base_detail_url: {}}
    appartements = {base_detail_url: {}}

    while True:
        page_url = f"{url}?page={page}"
        print(f"[INFO] Scraping: {page_url}")
        # Utiliser la fonction fetch_and_parse pour obtenir le contenu HTML
        soup = fetch_and_parse(page_url)
        ads = soup.select('.views-row')
        
        if not ads:
            print("[INFO] Plus d'annonces trouvées. Fin du scraping.")
            break
        
        # Trouver toutes les annonces
        for ad in ads :
            try:
            # Récupérer les informations nécessaires
                title = ad.select_one('.block-titre a').text.strip()
                price = ad.select_one('.block-price').text.strip()
                description = ad.select_one('.block-description p').text.strip()
                location = ad.select_one('.block-lieu div:last-child').text.strip()
                date = ad.select_one('.block-date time').text.strip()
                link = base_detail_url + ad.select_one('.block-titre a')['href']
            except AttributeError:
            # Ignorer les annonces mal formées
                print("Une annonce n'a pas pu être parsée correctement.")
                continue

            # Trier les annonces en fonction du type de logement
            if "appartement" in description.lower():
                logement  =   {
                    'id': compteur_appartement,
                    'Titre': title,
                    'Prix': price,
                    'Localisation': location,
                    'Type': 'appartement',
                    'Date': date,
                    'Lien': link               
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
                    'Date': date,
                    'Lien': link               
                }
                maisons[base_detail_url][f"logement {compteur_maison}"] = logement
                compteur_maison +=1
        page += 1

    # Enregistrer les données dans un fichier YAML
    save_to_yaml('maisons.yaml', maisons)
    save_to_yaml('appartements.yaml', appartements)   


if __name__ == "__main__":
    url = sys.argv[1]
    # Récupérer les annonces
    get_ads_0(url)
