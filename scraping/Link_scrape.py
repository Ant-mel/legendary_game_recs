import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

game_links = []

# On the last check, you only need to scrape the first 3337 pages before weird shit arrises
pages = range(1,3337,1)

for page in pages:
    resp = requests.get(f"https://www.backloggd.com/games/lib/release?page={page}")
    sop = BeautifulSoup(resp.content, 'html.parser')
    game_html = sop.find_all('div', class_='col-2 my-2 px-1 px-md-2')
    for game in game_html:
        link = game.find('a', href=True)['href']
        print(link)
        game_links.append(link)


with open('all_links_v2', 'wb') as all:
    pickle.dump(game_links, all)
