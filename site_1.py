import requests
from bs4 import BeautifulSoup
import PyYAML
import sys
import subprocess

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
    maisons_pavillons = []
    appartements = []
    maisons_yml = []

    # Afficher le contenu brut de la page
    # print("Contenu brut de la page HTML :")

    # Afficher des parties spécifiques du contenu
    print("\nOffres trouvés :")
    # Trouver les éléments d'annonces (par exemple, 'div' avec la classe 'views-row')
    ads = soup.find_all('div', class_='views-row')
    compteur_maison = 1
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
            maisons_pavillons.append((title, location, price, ad_type, link))
            logement  =   {
                'id': compteur_maison,
                'titre': title,
                'prix': ', '.join(price),
                'localisation': location,
                'type': ad_type,
                'lien': link
            }
            compteur_maison +=1
            maisons_yml.append(logement)
        else:
            appartements.append((title, location, price, ad_type, link))
    ads_bailleur_ = {url_bailleur: maisons_yml}
    # Enregistrer les données dans un fichier YAML
    with open('maisons.yaml', 'w') as file:
        PyYAML.dump(ads_bailleur_, file, default_flow_style=False, allow_unicode=True)
    subprocess.run(['cat', 'maisons.yaml'])
    # Afficher les résultats triés
    global_compteur = 1
    # print(soup)
    # Afficher les maisons et pavillons en premier
    print("\n################# Site 1" ,base_detail_url, "#" * 50)
    print("Maisons et Pavillons",url_bailleur)
    print('#' * 100)

    for title, location, price, ad_type, link in maisons_pavillons:
        print(f'### Offre {global_compteur}: ###')
        print(f"Titre : {title}")
        print(f"Prix : {', '.join(price)}")
        print(f"Localisation : {location}")
        print(f"Type : {ad_type}")
        print(f"Lien : {link}")
        print('-' * 50)
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



# Si ce fichier est exécuté directement, la fonction suivante sera appelée

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_1(url)