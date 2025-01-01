import os
import yaml

def save_to_yaml(file_path, data):
    """
    Sauvegarde les données dans un fichier YAML en préservant les données existantes.

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