import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pickle
import time
import csv

# Loading my link data
with open('all_links_v1', 'rb') as links:
    game_links = pickle.load(links)
frame = pd.DataFrame(game_links)

# Prepeing final list and setting count for montoring progress
# Only the first 116928 are relevant, and we will scrape in batches of 25000
missed_data = []
game_data = []
count = 0

for game in frame[0][100000:125000]:
    # Monitoring progress
    if count % 250 == True:
        print(count)
        print(game)
    else:
        pass
    count += 1

    try:
        # Setting up the html parser + beautful soup
        game_response = requests.get(f"https://www.backloggd.com{game}")
        game_soup = BeautifulSoup(game_response.content, 'html.parser')

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
        plays = counter[0].find('p', class_='mb-0').string
        playing = counter[1].find('p', class_='mb-0').string
        backlogs = counter[2].find('p', class_='mb-0').string
        wishlist = counter[3].find('p', class_='mb-0').string

        # Get a list of publishers
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

        total_lists = lists_reviews[0].get_text(strip=True).strip(" Lists")
        total_reviews = lists_reviews[1].get_text(strip=True).strip(" Reviews")

        # Get game category + main (If applicable)
        # If the search for category fails, then the game is the main game
        try:
            main_game = game_soup.find('p', class_='mb-2 game-parent-category').find('a').get_text()
            full_sentence = game_soup.find('p', class_='mb-2 game-parent-category').get_text()
            category = full_sentence.replace(main_game, '').strip()
        except:
            main_game = title
            category = 'main'

        game_data.append({'title': title,
                        'release_date': date_as_datetime,
                        'plays':plays,
                        'playing':playing,
                        'backlogs':backlogs,
                        'wishlist':wishlist,
                        'developers':publisher_list,
                        'avg_review':review_score,
                        'genres':genre_list,
                        'platforms':platform_list,
                        'description':description,
                        'total_reviews':total_reviews,
                        'total_lists':total_lists,
                        'category':category,
                        'main':main_game})
    except:
        print(f'Failed at {game}, count = {count}')
        missed_data.append(game)
        time.sleep(70)

game_df = pd.DataFrame(game_data)
game_df.to_csv('all_data_batch5', index=False)

with open ('missed_data_v5', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(missed_data)