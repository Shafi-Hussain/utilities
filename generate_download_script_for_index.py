import requests
from bs4 import BeautifulSoup

# Extra Index URL
URL = "http://localhost:8080/simple/{}/"

download_links = []
packages = list(map(lambda a: a.get_text(strip=True), BeautifulSoup(requests.get(URL.rstrip("{}/")).content, 'lxml').find_all('a')))

for pkg in packages:
    for a in BeautifulSoup(requests.get(URL.format(pkg)).content, 'lxml').find_all('a'):
        download_links.append((f"wheels/{a.get_text(strip=True)}", f"{URL.format(pkg)}{a['href']}"))

with open('download.sh', 'w') as f:
    f.write("\n".join(map(lambda z: f"curl -kL {z[1]} -o {z[0].split('#')[0]}", download_links)))
