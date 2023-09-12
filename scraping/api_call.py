import os
import sys
import pandas as pd
import requests
from igdb.wrapper import IGDBWrapper
import json
import matplotlib.pyplot as plt
sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *
from urllib.parse import quote

# Function that creates a list of features
def get_list_of_features(the_json):
    feature_dic = {"id":None,
        "aggregated_rating": None,
        "aggregated_rating_count": None,
        "game_engines": None,
        "game_modes": None,
        "player_perspectives": None,
        "themes": None,
        'rating': None}

    for key in the_json.keys():
        if type(the_json[key]) == list:
            for i in range(len(the_json[key])):
                value = the_json[key][i]['name']
                feature_dic.update({f'{key}': value})

        else:
            value = the_json[key]
            feature_dic.update({f'{key}': value})

    return feature_dic


# #Getting the data
# data = pd.read_csv('raw_data/all_game_data_v1', low_memory=False)
# df = cleaning_in_notebook(data)

# #Data with no reviews

# #Creating a mask
# df_mask = df['avg_review'] == 0
# df_no_reviews = df[df_mask]

# #Sorting and removing upcoming games to reduce load
# df_sorted = df_no_reviews.sort_values('release_date')
# time_mask = df_sorted['release_date'] < "2023-08-01"
# no_duplicates_recent_games = df_sorted[time_mask].drop_duplicates('title')
# list_of_titles_without_review = no_duplicates_recent_games['title']


# #Data with reviews
# df_good_mask = df['avg_review'] != 0
# df_with_reviews = df[df_good_mask]
# with_reviews_dropped_dupes = df_with_reviews.drop_duplicates('title')
# titles_with_reviews = with_reviews_dropped_dupes['title']

game_ids = pd.read_csv('raw_data/all_links_with_game_id_v1').drop_duplicates()
game_ids_list = game_ids['game_id']



# Credentials for calling the API
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GRANT_TYPE = os.getenv("GRANT_TYPE")

#Generating the access token
response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}')
response_json = response.json()
ACCESS_TOKEN = response_json['access_token']


#This is a wrapper from IGDB just for their API
wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

no_data = []
list_sons = []


for game in game_ids_list[110000:120096]:
    try:
        the_feat = json.loads(wrapper.api_request('games',
                f'fields age_ratings.rating, age_ratings.content_descriptions.category,aggregated_rating,aggregated_rating_count, game_engines.name, game_modes.name, multiplayer_modes, player_perspectives.name, themes.name, name, rating; where id = {game};'))
        list_sons.append(the_feat[0])

    except:
        print('fail')
        no_data.append(game)


with open('raw_data/api_json_110ktoEndk', 'w') as json_file:
    json.dump(list_sons, json_file)

missed = pd.DataFrame(no_data)
missed.to_csv('raw_data/api_json_missed_110ktoEndk', index=False)


# #This for loop runs game titles to get the data
# for game in titles_with_reviews[10000:20000]:
#     game_q = quote(game)

#     try:
#         the_feat = json.loads(wrapper.api_request('games',
#                         f'fields aggregated_rating,aggregated_rating_count, game_engines.name, game_modes.name, multiplayer_modes, player_perspectives.name, themes.name, rating; where name = "{game}";'))

#         v = get_list_of_features(the_feat[0])
#         v.update({'title':game})
#         list_dicts.append(v)

#     except:
#         print('fail')
#         no_data.append(game)

# the_frame = pd.DataFrame(list_dicts)
# the_frame.to_csv('raw_data/api_data_with_reviews_10to20k', index=False)

# missed = pd.DataFrame(no_data)
# missed.to_csv('raw_data/api_missed_data_with_reviews_10to20k', index=False)
