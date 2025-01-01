import requests
from bs4 import BeautifulSoup
import yaml
import sys
from save_to_yaml import save_to_yaml

def get_ads_1(url_bailleur):
    # URL de base pour les détails des logements, dérivé de url_bailleur
    base_detail_url = url_bailleur.replace('/biens?type_de_bien=hlm&louer_ou_acheter=acheter&', '')
    # En-têtes pour simuler un navigateur et éviter les blocages
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    # Faire une requête GET pour récupérer le contenu de la page
    response = requests.get(url_bailleur , headers=headers)
    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialiser les listes pour les types de logements
    maisons = {
        base_detail_url: {}
    }
    appartements = {
        base_detail_url: {}
    }
    # Afficher des parties spécifiques du contenu
    print("\nOffres trouvés :")
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

        # Trier les annonces en fonction du type de logement
        if "maison" in ad_type.lower() or "pavillon" in ad_type.lower():
            logement  =   {
                'id': compteur_maison,
                'titre': title,
                'prix': ', '.join(price),
                'localisation': location,
                'type': ad_type,
                'lien': link
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
                'Lien': link
            }
            compteur_appartement +=1
            appartements[base_detail_url][f"logement {compteur_appartement}"] = logement



    # Enregistrer les données dans un fichier YAML
    save_to_yaml('maisons.yaml', maisons)   


# Si ce fichier est exécuté directement, la fonction suivante sera appelée

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_1(url)