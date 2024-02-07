def drop_dot_make_int(string):
    """
    Removes '.' from summarised numbers, and drops the extra 0 to accomidate for it
    """

    if '.' in string:
        drop_dot = string.replace('.', '')[:-1]
        value = int(drop_dot)
    else:
        value = int(string)

    return value

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
    # original_json_df['age_ratings'] = original_json_df['age_ratings'].apply(get_category_descriptions)

    return original_json_df
