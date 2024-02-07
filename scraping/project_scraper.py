import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as datetime
import time

from google.cloud import bigquery
import os
import sys

from utils.scraping_and_api_utils import drop_dot_make_int

# Checks if a file exists. If the file exists then then this wont run
flag_file_path = "/app/flag_file.txt"

if os.path.exists(flag_file_path):
    print("Script has already been run. Exiting.")
    sys.exit(0)

client = bigquery.Client()

dataset = 'raw_data'
links_table = 'backlogged_game_links'
game_data_table = 'backlogged_game_data'
missed_data_table = 'backlogged_missed_data'

query = f"""SELECT * FROM `legendary-game-recs.game_data_01_24.game_links`"""

# Setting count for montoring progress
count = 0

query_job = client.query(query)
results = query_job.result()

data = results.to_dataframe()
frame = data.copy()

for game in frame['link']:
    # Monitoring progress
    if count % 10 == True:
        print(count)
    else:
        pass

    count += 1

    try:
        # Setting up the html parser + beautful soup
        game_response = requests.get(f"https://www.backloggd.com{game}")
        game_soup = BeautifulSoup(game_response.content, 'html.parser')


        # Scraping game_id
        game_id = game_soup.find('div', class_='card mx-auto game-cover overlay-hide')['game_id']


        # Scraping the title
        title = game_soup.find('h1', class_='mb-0').string

        # Scraping the date, and making it DateTime
        date_step = game_soup.find('div', class_='col-auto mt-auto pr-0')
        date_step2 = date_step.find('a', href=True).string
        if date_step2 == 'TBD':
            date_as_datetime = datetime.datetime(1, 1, 1).strftime("%Y-%m-%d")

        else:
            date_as_datetime = datetime.datetime.strptime(date_step2, '%b %d, %Y').strftime('%Y-%m-%d')


        # Getting the plays, playing, backlogs and wishlist information

        counter = game_soup.find('div', id='log-counters').find_all('a', class_='plays-counter')

        plays = drop_dot_make_int(counter[0].find('p', class_='mb-0').string.replace('K', '000'))
        playing = drop_dot_make_int(counter[1].find('p', class_='mb-0').string.replace('K', '000'))
        backlogs = drop_dot_make_int(counter[2].find('p', class_='mb-0').string.replace('K', '000'))
        wishlist = drop_dot_make_int(counter[3].find('p', class_='mb-0').string.replace('K', '000'))

        # Get a list of publis
        publisher_list = []
        try:
            publishers = game_soup.find('div', class_='col-auto pl-lg-1 sub-title').find_all('a', href=True)
            for i in range(len(publishers)):
                publisher_list.append(publishers[i].string)
        except:
            publisher_list = []

        # Get Average review score
        review_score = game_soup.find('h1', class_='text-center').string
        if review_score == 'N/A':
            review_score = 0
        else:
            review_score = float(review_score)

        # Get genres
        genres = game_soup.find_all('p', class_='genre-tag')
        genre_list = []
        for i in range(len(genres)):
            genre_list.append(genres[i].string)

        # Get platforms
        platforms = game_soup.find_all('a', class_='game-page-platform')
        platform_list = []
        for i in range(len(platforms)):
            platform_list.append(platforms[i].get_text(strip=True))

        # Get description
        description = game_soup.find('div', id='collapseSummary').get_text(strip=True)

        # Get number of reviews - number of lists associated is here as well
        lists_reviews = game_soup.find_all('p', class_='game-page-sidecard')

        total_lists = drop_dot_make_int(lists_reviews[0].get_text(strip=True).strip(" Lists").replace('K', '000'))
        total_reviews = drop_dot_make_int(lists_reviews[1].get_text(strip=True).strip(" Reviews").replace('K', '000'))

        # Get game category + main (If applicable)
        # If the search for category fails, then the game is the main game
        try:
            main_game = game_soup.find('p', class_='mb-2 game-parent-category').find('a').get_text()
            full_sentence = game_soup.find('p', class_='mb-2 game-parent-category').get_text()
            category = full_sentence.replace(main_game, '').strip()
        except:
            main_game = title
            category = 'main'

        # Get ratings, ten categories from 0.5 to 5.0

        ratings = game_soup.find_all('div', class_="col px-0 top-tooltip")

        ratings_zero_five = int(ratings[0]['data-tippy-content'].split(' |')[0])
        ratings_one_zero = int(ratings[1]['data-tippy-content'].split(' |')[0])
        ratings_one_five = int(ratings[2]['data-tippy-content'].split(' |')[0])
        ratings_two_zero = int(ratings[3]['data-tippy-content'].split(' |')[0])
        ratings_two_five = int(ratings[4]['data-tippy-content'].split(' |')[0])
        ratings_three_zero = int(ratings[5]['data-tippy-content'].split(' |')[0])
        ratings_three_five = int(ratings[6]['data-tippy-content'].split(' |')[0])
        ratings_four_zero = int(ratings[7]['data-tippy-content'].split(' |')[0])
        ratings_four_five = int(ratings[8]['data-tippy-content'].split(' |')[0])
        ratings_five_zero = int(ratings[9]['data-tippy-content'].split(' |')[0])

        # Creating a dictionary to insert into GCP
        data_dict = {'title': title,
                        'release_date': date_as_datetime,
                        'plays':plays,
                        'playing':playing,
                        'backlogs':backlogs,
                        'wishlist':wishlist,
                        'developers':str(publisher_list),
                        'avg_review':review_score,
                        'genres':str(genre_list),
                        'platforms':str(platform_list),
                        'description':description,
                        'total_reviews':total_reviews,
                        'total_lists':total_lists,
                        'category':category,
                        'main':main_game,
                        'ratings_zero_five':ratings_zero_five,
                        'ratings_one_zero':ratings_one_zero,
                        'ratings_one_five':ratings_one_five,
                        'ratings_two_zero':ratings_two_zero,
                        'ratings_two_five':ratings_two_five,
                        'ratings_three_zero':ratings_three_zero,
                        'ratings_three_five':ratings_three_five,
                        'ratings_four_zero':ratings_four_zero,
                        'ratings_four_five':ratings_four_five,
                        'ratings_five_zero':ratings_five_zero,
                        'url':game,
                        'game_id':game_id}

        # Inserting into GCP
        table = client.dataset(dataset).table('game_data')
        errors = client.insert_rows_json(table, [data_dict])

        # Relaying errors for some sexy debugging
        if errors:
            print(f'Failed {game}, {errors}')
            #Saving missed data, so we can try get it later
            table = client.dataset(dataset).table('missed_data')
            errors = client.insert_rows_json(table, [{'link':game}])
        else:
            print(f'all good {count}')


    except:
        # Relaying when Backlogged rejects us
        print(f'Page failure at {game}, count = {count}')
        #Saving missed data, so we can try get it later
        table = client.dataset(dataset).table('missed_data')
        errors = client.insert_rows_json(table, [{'link':game}])

        time.sleep(3)


with open(flag_file_path, "w") as flag_file:
    flag_file.write("Script has been run")
