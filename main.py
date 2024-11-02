from site_1 import get_ads_1
from site_2 import get_ads_2
import os
import sys
import subprocess

def main():
    url_bailleur_1 = os.getenv('URL_BAILLEUR_1')
    url_bailleur_2 = os.getenv('URL_BAILLEUR_2')
    


#    print("\n################# Site 1 #################")
    subprocess.run(["python", "site_1.py", url_bailleur_1])
    
#    print("\n################# site 2 #################\n")
    get_ads_2(url_bailleur_2)

if __name__ == "__main__":
    main()
