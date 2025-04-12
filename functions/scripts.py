import re

###################################################
# site_1.py
###################################################

def extract_number_from_type(ad_type):
    # Utiliser une expression régulière pour extraire le premier nombre trouvé dans la chaîne
    match = re.search(r'\d+', ad_type)
    if match:
        return int(match.group())
    return None

###################################################
# site_2.py
###################################################

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

###################################################
# site_5.py
###################################################

# Dictionary of Île-de-France departments with their postal codes
ILE_DE_FRANCE_DEPTS = {
    '75': 'Paris',
    '77': 'Seine-et-Marne',
    '78': 'Yvelines',
    '91': 'Essonne',
    '92': 'Hauts-de-Seine',
    '93': 'Seine-Saint-Denis',
    '94': 'Val-de-Marne',
    '95': 'Val-d\'Oise'
}

# function to check locations
def is_in_ile_de_france(location):
    """Check if the location is in Île-de-France based on postal code"""
    # Extract postal code using regex (looking for 5 digits)
    postal_code_match = re.search(r'\b(\d{5})\b', location)
    if postal_code_match:
        postal_code = postal_code_match.group(1)
        # Get department code (first two digits of postal code)
        dept_code = postal_code[:2]
        # Special case for Corsica (2A, 2B) and overseas departments
        if dept_code == '20' or dept_code == '97':
            return False
        return dept_code in ILE_DE_FRANCE_DEPTS
    return False
