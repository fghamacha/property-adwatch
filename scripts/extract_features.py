import re

def extract_features(features):
    # Extraire le prix
    price_match = re.search(r'(\d+\s*\d*)\s*€', features)
    price = price_match.group(1).replace(' ', '') if price_match else None

    # Extraire le nombre de chambres
    rooms_match = re.search(r',\s*(\d+)\s*,', features)
    rooms = int(rooms_match.group(1)) if rooms_match else None

    # Extraire la surface
    surface_match = re.search(r'(\d+\s*\d*)\s*m2', features)
    surface = surface_match.group(1).replace(' ', '') if surface_match else None

    return price, rooms, surface