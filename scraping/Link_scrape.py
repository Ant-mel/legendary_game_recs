import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery
from flask import Flask
import os

app = Flask(__name__)

# Use the default credentials when running in Google Cloud Run
client = bigquery.Client()

@app.route('/')
def scrape_and_store():
    pages = range(1, 3300, 1)
    links_id = []

    for page in pages:
        resp = requests.get(f"https://www.backloggd.com/games/lib/release?page={page}")
        sop = BeautifulSoup(resp.content, 'html.parser')
        game_html = sop.find_all('div', class_='card mx-auto game-cover quick-access')

        for game in game_html:
            link = game.find('a', href=True)['href']
            game_id = game['game_id']

            links_id.append({'link': link, 'game_id': game_id})

    the_frame = pd.DataFrame(links_id)
    dataset_ref = client.dataset('raw_data')
    table_ref = dataset_ref.table('backlogged_game_links')

    job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
    job = client.load_table_from_dataframe(the_frame, table_ref, job_config=job_config)

    return "Scraping and storing completed successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
