import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery

import os

client = bigquery.Client.from_service_account_json(os.getenv('JSON_KEY'))

# On the last check, you only need to scrape the first 3337 pages before weird shit arrises
pages = range(40,50,1)

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

    print(page)

#Saves to dataframe then stores on GCP
the_frame = pd.DataFrame(links_id)
dataset_ref = client.dataset('game_links_test')  # Replace with your dataset name
table_ref = dataset_ref.table('test_links_v1')

job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')  # Overwrite existing table
job = client.load_table_from_dataframe(the_frame, table_ref, job_config=job_config)
