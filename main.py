import os
import sys
import subprocess
from dotenv import load_dotenv
import platform  # Pour détecter le système d'exploitation



load_dotenv()  # Charger les variables d'environnement

def main():
    url_bailleur_1 = os.getenv('URL_BAILLEUR_1')
    url_bailleur_2 = os.getenv('URL_BAILLEUR_2')
    url_bailleur_4 = os.getenv('URL_BAILLEUR_4')
   
#    print("\n################# Site 1 #################")
    subprocess.run(["python", "site_1.py", url_bailleur_1])
    
#    print("\n################# site 2 #################\n")
    subprocess.run(["python", "site_2.py", url_bailleur_2])

#    print("\n################# site 4 #################\n")
    subprocess.run(["python", "site_4.py", url_bailleur_4])

#    print("\n################# Maisons yml #################\n")
    # Afficher le contenu de maisons.yaml en fonction du système d'exploitation
    if platform.system() == "Windows":
        subprocess.run(['type', 'maisons.yaml'], shell=True)
    else:
        subprocess.run(['cat', 'maisons.yaml'], shell=True)


if __name__ == "__main__":
    main()
