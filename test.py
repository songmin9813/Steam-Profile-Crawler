import requests
from bs4 import BeautifulSoup

webpage = requests.get("https://steamcommunity.com/id/songmin9813/games/?tab=all")
soup=BeautifulSoup(webpage.content, "html.parser")
print(soup.find_all(attrs={'class':''}))