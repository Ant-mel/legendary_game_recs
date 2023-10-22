import os
import sys
import pandas as pd
import requests
from igdb.wrapper import IGDBWrapper
import json
import matplotlib.pyplot as plt
sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *

# Function that creates a list of features
def get_list_of_features(the_json):
    feature_dic = {"id":None,
        "aggregated_rating": None,
        "aggregated_rating_count": None,
        "game_engines": None,
        "game_modes": None,
        "player_perspectives": None,
        'multiplayer_modes': None,
        "themes": None,
        'rating': None,
        'franchise': None,
        'franchises': None,
        'storyline': None}

    for key in the_json.keys():
        if type(the_json[key]) == list:
            for i in range(len(the_json[key])):
                value = the_json[key][i]['name']
                feature_dic.update({f'{key}': value})

        else:
            value = the_json[key]
            feature_dic.update({f'{key}': value})

    return feature_dic


# List of games used in the model
game_df= pd.read_json('raw_data/final_data')
list_of_game_id = game_df['game_id']



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

for game in list_of_game_id:
    try:
        the_feat = json.loads(wrapper.api_request('games',
                f'fields franchise, franchises, storyline, aggregated_rating,aggregated_rating_count, game_engines.name, game_modes.name, multiplayer_modes, player_perspectives.name, themes.name, rating; where id = {int(game)};'))
        list_sons.append(the_feat[0])

    except:
        print('fail')
        no_data.append(game)


with open('raw_data/final_api_call', 'w') as json_file:
    json.dump(list_sons, json_file)

missed = pd.DataFrame(no_data)
missed.to_csv('raw_data/final_api_call_missed_games', index=False)
