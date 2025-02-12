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

# Exemple d'utilisation
features = "230 490 €, 3, 65 m2"
price, rooms, surface = extract_features(features)
print(f"Prix: {price} €")
print(f"Nombre de chambres: {rooms}")
print(f"Surface: {surface} m2")
