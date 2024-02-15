import pandas as pd
from datetime import datetime

from sklearn.preprocessing import MultiLabelBinarizer,PowerTransformer


def make_stringlist_list(string):
    '''
    Removes square brackets, and splits the string by comma to the create a list
    '''
    list_of_strings = string[2:-2].replace("'", '').split(',')
    return list_of_strings

def remove_whitespace(list_):
    '''
    Removes whitesapces from items within lists
    '''
    empty = []

    for i in range(len(list_)):
        item = list_[i].strip()
        empty.append(item)
    return empty

def clean_stringlists(df):
    '''
    For lists that were imported as strings, this removes square brackers
    and cleans up trailing whitespaces
    '''
    string_to_list_df = df.apply(make_stringlist_list)
    remove_whitespace_df = string_to_list_df.apply(remove_whitespace)

    return remove_whitespace_df

def make_list_columns_to_lists(df, columns):
    '''
    This returns a dataframe of columns where lists where imported as strings,
    and returns them to their list state
    '''
    cleaned_df = pd.DataFrame()

    for col in columns:
        cleaned = clean_stringlists(df[col])
        cleaned_df[col] = cleaned
    return cleaned_df


def only_main_games(df):
    """
    Filters the dataframe for only main games
    """
    main_game_mask =df['category'] == 'main'
    only_main_games = df[main_game_mask]

    return only_main_games.drop('category', axis=1)


def process_raw_data(data, year, month, day, list_of_multicategorical_columns):
    """
    This cleans and seperates the data into
    upcoming games and released games
    I realised you can do all of this with a SQL query...
    So only a few parts relevant now - the rest hashed out
    """

    # # Dropping duplicates
    working_data = data.copy()
    # working_data.drop_duplicates(subset=['game_id'],inplace=True)

    # Turning categorical features into lists (they arrive as strings that look like lists)
    string_to_list_colums = list_of_multicategorical_columns
    working_data[string_to_list_colums] = make_list_columns_to_lists(working_data, string_to_list_colums)

    # # Changining release_date to a datetime so we can filter it later
    # working_data['release_date'] = pd.to_datetime(working_data['release_date'], errors='coerce')

    # # Removing games wuth no release date.
    # year_1_mask = working_data['release_date'].isna()
    # games_that_exist = working_data[~year_1_mask]

    # # Removing DLCs, Mods and the such
    # only_main_games_df = only_main_games(games_that_exist)

    # Splitting the data into upcoming games and TBC games.
    upcoming_mask = working_data['release_date'] > pd.Timestamp(datetime(year, month, day))
    upcoming_games = working_data[upcoming_mask]
    released_games = working_data[~upcoming_mask]

    # # Selecting games with reviews, otherwise no one wants to play them.
    # released_games_with_reviews = released_games[released_games['avg_review'] > 0].copy()

    return released_games, upcoming_games


def multilable_encoding(data, column):
    """
    This ohe encodes categories that are stored in lists
    """
    # Initilizing encoder and transforming the data
    mlb_genre = MultiLabelBinarizer()
    transformed_genre = mlb_genre.fit_transform(data[column])

    # Labeling newly created features
    genre_ohe_colums = pd.DataFrame(transformed_genre, columns=mlb_genre.classes_)
    # Concatinating the data
    droped_columns = data.drop(column, axis=1).copy()
    scaled_data = pd.concat((droped_columns, genre_ohe_colums), axis=1)

    scaled_data.rename(columns={'':f'NaN_{column}',}, inplace=True)

    return scaled_data

def yeo_johnson_scaling(X_train, column):
  """
  Scales the specified column using Yeo-Johnson method (PowerTransformer).
  """
  transformer = PowerTransformer(method='yeo-johnson', standardize=False)
  transformed_column = transformer.fit_transform(X_train[[column]]).squeeze()
  X_train[column] = transformed_column
  return X_train
