import pandas as pd
import requests
from igdb.wrapper import IGDBWrapper
import json

# Function that creates a list of features
def get_list_of_features(the_json,igdb_feature_name):
    feature_list = []

    for i in range(len(the_json[0][igdb_feature_name])):
        feat = the_json[0][igdb_feature_name][i]['name']
        feature_list.append(feat)

    return feature_list


# Credentials for calling the API
response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}')
response_json = response.json()


ACCESS_TOKEN = response_json['access_token']



wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

no_reviews = []
no_data = []

for game in no_review_titles[1620:8520]:
    features = json.loads(wrapper.api_request('games',
                    'fields aggregated_rating,aggregated_rating_count, game_engines.name, game_modes.name, multiplayer_modes, player_perspectives.name, themes.name, rating; where name = "{game}";'))

    if len(features) == 0:
        no_data.append(game)

    else:
        game_id = features[0]['id']
        critic_rating = features[0]['aggregated_rating']
        number_of_critics = features[0]['aggregated_rating_count']
        game_engines = get_list_of_features(features, 'game_engines')
        game_modes = get_list_of_features(features, 'game_modes')
        player_perspectives = get_list_of_features(features, 'player_perspectives')
        themes = get_list_of_features(features, 'themes')

        no_reviews.append({'game_id': game_id,
                'critic_rating':critic_rating,
                'number of critics' :number_of_critics,
                'game_engines':game_engines,
                'game_modes':game_modes,
                'player_perspectives': player_perspectives,
                'themes': themes})
