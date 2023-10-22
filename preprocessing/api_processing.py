import sys
import pandas as pd

sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *
from preprocessing.preprocess_2_features import *
from preprocessing.pipeline_the_unification import *


#Columns we would want to drop
api_cols_to_drop = ['game_engines', 'aggregated_rating', 'rating',
                    'aggregated_rating_count', 'age_ratings', 'multiplayer_modes']

extra_cols_to_drop = ['link', 'game_id', 'id', 'game_modes',
                      'name', 'themes', 'player_perspectives']

# Cleans links for easy merging with Backlogged Data - there are two options
# Option 1
def remove_link_trail(string):
    update = string.replace('https://www.backloggd.com', '')
    return update

# Option 2
def clean_urls(url):
    shorter_url = url[25:]

    return shorter_url

# This is used for getting the information from age_ratings.
def get_category_descriptions(json_dict):
    category_list = []

    if type(json_dict) == float:
        category_list = None
    else:
        for i in range(len(json_dict)):
            try:
                descriptions = json_dict[i]['content_descriptions']
                for i in range(len(descriptions)):
                    rating_descript = descriptions[i]['category']
                    category_list.append(rating_descript)

            except:
                pass

    return category_list

# This goes through each key in the JSON and creates a list of items for the variable
def get_names_from_dict(dict_list):
    list_of_items = []
    try:
        for i in range(len(dict_list)):
            item = dict_list[i]['name']
            list_of_items.append(item)
    except:
        list_of_items = None

    return list_of_items

# This uses the above functions to create a final, clean df
def prepare_json_df(original_json_df):
    original_json_df['themes'] = original_json_df['themes'].apply(get_names_from_dict)
    original_json_df['game_modes'] = original_json_df['game_modes'].apply(get_names_from_dict)
    original_json_df['player_perspectives'] = original_json_df['player_perspectives'].apply(get_names_from_dict)
    original_json_df['game_engines'] = original_json_df['game_engines'].apply(get_names_from_dict)
    original_json_df['age_ratings'] = original_json_df['age_ratings'].apply(get_category_descriptions)

    return original_json_df

# This merges the API data with the raw data, using link data as a proxy
def encode_api_data(raw_data, link_data, api_data):
    reference = pipeline_genre_ohe_only(raw_data)
    reference['url'] = reference['url'].apply(remove_link_trail)

    data_with_id = reference.merge(link_data, left_on='url', right_on='link')
    all_data = data_with_id.merge(api_data, left_on='game_id', right_on='id')

    prepped_data = prepare_json_df(all_data)
    nec_data = prepped_data.drop(api_cols_to_drop, axis=1)
    filled_data = nec_data.fillna('')

    ohe_modes, mlb = categorical_encoder(filled_data['game_modes'])
    ohe_theme= keeping_ohe_columns_and_dropping_the_originals(filled_data[['themes']], 16)
    ohe_perspect, mlb = categorical_encoder(filled_data['player_perspectives'])

    ohe_colums = pd.concat((ohe_modes, ohe_theme, ohe_perspect), axis=1)

    everything = pd.concat((filled_data, ohe_colums), axis=1)

    return everything.drop(extra_cols_to_drop, axis=1)


def ohe_api_category(data, column_name):
    """
    Returns OHE columns of api categories
    """
    data[column_name] = data[column_name].apply(get_names_from_dict)

    ohes, mlb = categorical_encoder(data[column_name])

    return ohes
