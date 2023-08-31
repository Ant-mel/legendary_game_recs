import requests
from bs4 import BeautifulSoup

url = "https://https://www.backloggd.com/games/the-legend-of-zelda-breath-of-the-wild/"
response = requests.get(url)

soup = BeautifulSoup(html, "html.parser")
title = url.find('h1', class_= 'mb-0').string.strip()
rate05 = article.find('div', class_= 'col px-0 top-tooltip" data-tippy-content=').string.strip()
print(title)
print(rate05)
