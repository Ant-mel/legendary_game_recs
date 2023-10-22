import pandas as pd

#RATINGS CATEGORIES

def get_category_descriptions(json_dict):
    '''
    This function only works on ratings_categories
    it ignores ratings and only returns the categories (which are floats)
    This is because I decided that the ratings are more useful in this moment
    '''
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

#UNPACK ALL OTHER FEATURES

def get_names_from_dict(dict_list):
    """
    This function is able to unpack all other features
    This excludes age_ratings and multiplayer_modes
    although if multiplayer_modes is re_scraped then it may work depending on format
    """
    list_of_items = []
    try:
        for i in range(len(dict_list)):
            item = dict_list[i]['name']
            list_of_items.append(item)
    except:
        list_of_items.append('')

    return list_of_items


#FINAL FUNCTION
def prepare_json_df(original_json_df):
    """
    This runs the appropriate function on the appropriate column and transforms them into lists
    This drops mulitplayer_modes, as information is not fetchable at the moment
    """

    original_json_df['themes'] = original_json_df['themes'].apply(get_names_from_dict)
    original_json_df['game_modes'] = original_json_df['game_modes'].apply(get_names_from_dict)
    original_json_df['player_perspectives'] = original_json_df['player_perspectives'].apply(get_names_from_dict)
    original_json_df['game_engines'] = original_json_df['game_engines'].apply(get_names_from_dict)
    original_json_df['age_ratings'] = original_json_df['age_ratings'].apply(get_category_descriptions)

    return original_json_df.drop('multiplayer_modes', axis=1)
