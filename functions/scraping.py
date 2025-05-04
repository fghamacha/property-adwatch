import requests
from bs4 import BeautifulSoup

import os
import yaml

import re


# En-têtes par défaut pour simuler une requête provenant d'un navigateur
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}
#  Fetch the content of a web page and parse it using BeautifulSoup.

def fetch_and_parse(url, headers=DEFAULT_HEADERS):

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        response.raise_for_status()


# Sauvegarde les données dans un fichier YAML en préservant les données existantes.

def save_to_yaml(file_path, data):
    """

    :param file_path: Chemin du fichier YAML.
    :param data: Données à ajouter au fichier.
    """
    # Charger les données existantes
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            existing_data = yaml.safe_load(file) or {}  # Charger un dict vide si le fichier est vide
    else:
        existing_data = {}

    # Fusionner les nouvelles données avec les données existantes
    existing_data.update(data)

    # Sauvegarder les données mises à jour dans le fichier YAML
    with open(file_path, 'w', encoding="utf-8") as file:
        yaml.dump(existing_data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)


def extract_surface(description):
    """Extrait la surface depuis la description"""
    match = re.search(r'(\d+[,\d]*)\s*m²', description)
    return match.group(1).replace(',', '.') if match else None

def extract_visit_dates(description):
    """Extrait les dates de visite de manière plus robuste"""
    visits = []
    # Pattern simplifié et plus robuste
    pattern = r'(?:VISITES?|VISITE)\s(?:SANS RDV\s*:?)?\s*([A-Z]+\s\d+\s[A-Z]+(?:\sET\s[A-Z]+\s\d+\s[A-Z]+)*)\s(?:DE\s(\d+H)\sA\s(\d+H))'
    
    for match in re.finditer(pattern, description, re.IGNORECASE):
        dates = match.group(1)
        hours = f"{match.group(2)}-{match.group(3)}"
        for date in re.split(r'\sET\s|,\s', dates):
            visits.append(f"{date.strip()} {hours}")
    
    return visits if visits else None