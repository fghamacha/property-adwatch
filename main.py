import os
import sys
import subprocess

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
    subprocess.run(['cat', 'maisons.yaml'])


if __name__ == "__main__":
    main()
