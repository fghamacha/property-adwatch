# scripts/extract_number_from_type.py

import re

def extract_number_from_type(ad_type):
    # Utiliser une expression régulière pour extraire le premier nombre trouvé dans la chaîne
    match = re.search(r'\d+', ad_type)
    if match:
        return int(match.group())
    return None
