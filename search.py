from googlesearch import search
from bs4 import BeautifulSoup
import requests
import re

import warnings
warnings.filterwarnings('ignore')

anchors = ["aviso-legal","politica-privacidad", "legal-warning"]
batons = ["CIF","C.I.F","NIF","N.I.F"]

def clean_cif(substring):
    substring = substring.strip()
    substring = substring.replace(" ","")
    substring = substring.replace(".","")
    substring = substring.replace("-","")
    substring = substring.replace("/","")
    substring = substring.replace(":","")

    # Find a letter and number adjoined
    for i in range(len(substring)-1):
        if substring[i].isalpha() and substring[i+1].isnumeric():
            substring = substring[i:]
            break

    # Find where the last 2 characters are numbers
    for i in range(len(substring)-1,0,-1):
        if substring[i].isnumeric() and substring[i-1].isnumeric():
            substring = substring[:i+1]
            break

    return substring

def check_cif(cif):

    # First character
    first_letter = cif[0]
    if not first_letter.isalpha():
        return False
    
    # Check rest of characters
    rest = cif[1:]
    if not rest.isnumeric():
        return False
    
    # Length
    if len(cif) != 9:
        return False

    return True

def find_cif(url):
    cif = None

    for anchor in anchors:
        target_url = url + "/" + anchor
        found = False # flag
        
        for baton in batons:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            
            # Make req
            try:
                resp = requests.get(target_url, headers=headers, verify=False, timeout=(1, 3))
            except Exception as e:
                print(str(e))
                continue
            
            # Look for baton
            soup = BeautifulSoup(resp.text, 'html.parser')
            text = soup.get_text()
            baton_found = re.search(baton, text)

            # Find and process NIF
            if baton_found:
                substring = text[baton_found.end():baton_found.end()+20]
                cif = clean_cif(substring)
                if check_cif(cif):
                    print(cif)
                    found = True
                    break # Break baton loop
        if found:
            break # Break anchor loop
    
    return cif

def google_search(q, num=10, stop=50, country="spain"):
    urls = [] # initialise check
    cifs = []

    # Generator object from the search
    for url in search(q, num=num, stop=stop, country=country):

        # Trim URL because of pages landing in SERP
        url = "https://"+ url.split("/")[2]
        print("URL: ",url)

        # check if url has been checked
        if url in urls:
            print("Skipping: ",url)
            continue
        else:
            urls.append(url)

        cif = find_cif(url)
        if cif:
            cifs.append(cif)

    return cifs