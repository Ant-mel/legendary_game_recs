import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

# On the last check, you only need to scrape the first 3337 pages before weird shit arrises
pages = range(1,3337,1)

#Creating an empty list to add the dicts to
links_id = []

for page in pages:
    #Creates the response
    resp = requests.get(f"https://www.backloggd.com/games/lib/release?page={page}")
    sop = BeautifulSoup(resp.content, 'html.parser')

    #Gets the HTML from the page
    game_html = sop.find_all('div', class_='card mx-auto game-cover quick-access')

    #Goes through all 36 games on the page, and gets info
    for game in game_html:
        #Scraping the Backloggd page link and IGDB game_id
        link = game.find('a', href=True)['href']
        id = game['game_id']


        links_id.append({'link':link,
                        'game_id':id})

#Saves to dataframe then stores as csv
the_frame = pd.DataFrame(links_id)
the_frame.to_csv('../raw_data/all_links_test', index=False)
