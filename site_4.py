import requests
from bs4 import BeautifulSoup
import sys

def get_ads_4(url_bailleur):
    # URL de base pour les détails des logements, dérivé de url_bailleur
    base_detail_url = url_bailleur.replace('rechercher?distance=0km&place=%C3%8Ele-de-France&place=%C3%8ELE-DE-FRANCE%3AIDF&tab=PURCHASE&type=Maison', '')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    # Faire une requête GET pour récupérer le contenu de la page
    response = requests.get(url_bailleur, headers=headers)
    
    # Analyser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    body_content = soup.body
    # Initialiser les listes pour les types de logements
    maisons_pavillons = []
    appartements = []

    logements = soup.find_all('a', class_="text-blue font-bold")
    print(logements)
    
        # Afficher des parties spécifiques du contenu
    # print("\nOffres trouvés :")
    # Trouver les éléments d'annonces (par exemple, 'div' avec la classe 'views-row')
    # ads = soup.find_all('div', class_='text-blue font-bold')
    # for ad in ads:
    #     title = ad.find('div', class_='field--name-field-titre-de-l-annonce').text.strip() if ad.find('div', class_='field--name-field-titre-de-l-annonce') else 'Titre non disponible'
    #     location = ad.find('span', class_="text-pink font-medium text-sm").text.strip() if ad.find('span', class_="text-pink font-medium text-sm") else 'Localisation non disponible'
    #     price = [li.text.strip() for li in ad.find_all('li') if 'Prix de vente' in li.text]
    #     attribs = ad.find('ul', class_='attributs line_ul')
    #      # Récupérer le lien de l'annonce
    #     link_tag = ad.find('a', class_='orange ft-14 parking-teaser_more underlined')
    #     link = base_detail_url + link_tag['href'] if link_tag else 'Lien non disponible'

    # Si ce fichier est exécuté directement, la fonction suivante sera appelée

if __name__ == "__main__":
    url = sys.argv[1]
    get_ads_4(url)