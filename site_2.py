import requests
from bs4 import BeautifulSoup
import yaml
import sys
from save_to_yaml import save_to_yaml



def get_ads_2(url_bailleur):
    # URL de base pour les détails des logements, dérivé de url_bailleur
    base_detail_url = url_bailleur.replace('resultats-vente-{}-defaut-', '{}')

    # Initialiser le compteur de pages
    page_number = 1
    compteur_maison = 1
    compteur_appartement = 1
    # Initialiser les listes pour les types de logements
    maisons_pavillons = []
    appartements = []
    maisons_yml = []
    appartements_yml = [] 
    
    # Liste des préfixes de codes postaux pour l'Île-de-France
    idf_prefixes = ['75', '77', '78', '91', '92', '93', '94', '95']

    while True:
        # Construire l'URL pour la page actuelle
        url = url_bailleur.format(page_number)
        
        # Envoyer une requête HTTP GET à la page
        response = requests.get(url)
        
        # Vérifier si la requête a réussi
        if response.status_code != 200:
            print(f"Erreur: Impossible d'accéder à la page {page_number} (status code {response.status_code})")
            break
        
        # Parser le contenu HTML de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver toutes les annonces de logements sur cette page
        ads = soup.find_all('div', class_='col-xs-12 col-sm-12 col-md-6 col-lg-6')
        
        # Si aucun logement n'est trouvé, sortir de la boucle
        if not ads:
        #    print("Aucune nouvelle offre trouvée, fin de la pagination.")
            break
        
        # Parcourir chaque annonce et extraire les informations
        for ad in ads:
            title = ad.find('h2')
            if title:
                title_text = title.text.strip()
                price = ad.find('span', class_='custom-figPrice').text.strip() if ad.find('span', class_='custom-figPrice') else "No Price"
                location = ad.find('div', class_='cardAddress').text.strip() if ad.find('div', class_='cardAddress') else "No Location"
                
                # Extraire le lien vers la page de détail
                link = ad.find('a', class_='card')['href']
                full_link = base_detail_url.format(link)
                
                # Vérifier si le logement est en Île-de-France
                if any(location.startswith(prefix) for prefix in idf_prefixes):
                    # Récupérer les caractéristiques et les nettoyer
                    features_list = ad.find('ul', class_='cardFeat')
                    if features_list:
                        features = ', '.join(item.text.strip() for item in features_list.find_all('li'))
                    else:
                        features = "No Features"
                    
                    # Trier les logements en fonction du type (maison/pavillon en premier)
                    if "maison" in title_text.lower() or "pavillon" in title_text.lower():
                        maisons_pavillons.append((title_text, price, location, features, full_link))
                        logement  =   {
                            'id': compteur_maison,
#                           'titre': title,
                            'prix': price,
                            'localisation': location,
                            'type': features,
                            'lien': full_link
                        }
                        compteur_maison +=1
                        maisons_yml.append(logement)
                    else:
                        appartements.append((title_text, price, location, features, full_link))

            # apparts_bailleur_ = {url_bailleur: appartements_yml}

        # Passer à la page suivante
        page_number += 1
                # create maisons.yaml file content
    ads_bailleur_ = {base_detail_url: maisons_yml}
    # Enregistrer les données dans un fichier YAML
    
    save_to_yaml('maisons.yaml', ads_bailleur_)


    

# Si ce fichier est exécuté directement, la fonction suivante sera appelée

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_2(url)