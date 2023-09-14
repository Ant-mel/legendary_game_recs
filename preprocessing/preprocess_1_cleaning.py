import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import datetime
from preprocessing.preprocess_2_features import create_gen, create_gen_3


# After importing a dataframe (df) from the raw data csv, run
# game_df = cleaning_in_notebook(df)
# **We are chaining copies of the original df so it is advisable to assign the
# cleaned dataframe as a new variable


# ONLY MAIN GAMES
# This function removes everything that is not a main game
def only_main_games(df):
    main_game_mask =df['category'] == 'main'
    only_main_games = df[main_game_mask]

    return only_main_games.drop('category', axis=1)


# DELETING ROWS

# The below functions delete: duplicates; games with no release dates

def drop_duplicates(df):
    '''This function deletes duplicates'''
    df.sort_values('title')
    return df.drop_duplicates()

def drop_no_release_date(df):
    '''This function deletes games with no release date'''
    df = df[df['release_date'] != "0001-01-01"]
    return df


# STRING PROCESSING

# The below functions clean Genres, Platforms, Developer columns
# Only the last function matters - make_list_column_to_lists
# It runs all the ones above it
def make_stringlist_list(string):
    '''This removes square brackets, and splits the string by comma to the create a list'''
    list_of_strings = string[2:-2].replace("'", '').split(',')
    return list_of_strings

def remove_whitespace(list_):
    '''This removes whitesapces from items within lists'''
    empty = []

    for i in range(len(list_)):
        item = list_[i].strip()
        empty.append(item)
    return empty

def clean_stringlists(df):
    '''For lists that were imported as strings, this removes square brackers and cleans up trailing whitespaces'''
    string_to_list_df = df.apply(make_stringlist_list)
    remove_whitespace_df = string_to_list_df.apply(remove_whitespace)

    return remove_whitespace_df

# This is the final one mentioned above
# string_columns = ['developers','genres','platforms']
def make_list_columns_to_lists(df, columns):
    '''This returns a dataframe of columns where lists where imported as strings, and returns them to their list state'''
    cleaned_df = pd.DataFrame()

    for col in columns:
        cleaned = clean_stringlists(df[col])
        cleaned_df[col] = cleaned
    return cleaned_df

# NUMERIC PROCESSING

# The below functions clean Plays, Playing, Backlogs, Wishlist,
# Total_Reviews, Total_Lists columns
# Only the last function matters - numeric_objects_reformatted
# It runs all the ones above it

def thousands_converter(x):
    '''This function removes the K and . from objects such as 4.1K, replacing with 4100'''
    if 'K' in x and '.' in x:
        x = x.replace('K', '00')
        x = x.replace('.','')
        return x
    elif 'K' in x:
        return x.replace('K','000')
    else:
        return x

#def remove_K(x):
 #   '''This function removes the K from objscts such as 92K, replacing with 92000'''
  #  if
   # else:
    #    return x

#This is the final function for use on numeric columns
# numeric_columns = ['plays','playing','backlogs','wishlist','total_reviews','total_lists']
def numeric_objects_reformatted(df, column):
    '''This function applies the removal of K and . above in order, and returns as integers'''
    df[column] = df[column].apply(thousands_converter)
    df[column] = df[column].astype('int')
    return df


# DATETIME PROCESSING

#The below changes the type of the release_date column

def change_to_datetype(df, column):
    df[column]=pd.to_datetime(df[column])
    return df

# DELETING NULL RELEASE DATES

# The below function removes games with no release date

def delete_no_release_date(df):
    return df[df['release_date'] != "null"]

# REMOVING NO REVIEWS

# This function removes rows with no avg_review
def remove_no_reviews(df):
    df_good_mask = df['avg_review'] != 0
    df_with_reviews = df[df_good_mask]

    return df_with_reviews

# REMOVING UNNECESARY COLUMNS

def drop_unnecesary_coulumns(df):
    cols_to_drop = ['developers', 'platforms',
                    'ratings_one_zero', 'ratings_one_five',
                    'ratings_two_zero', 'ratings_two_five',
                    'ratings_three_zero', 'ratings_three_five',
                    'ratings_four_zero', 'ratings_four_five',
                    'ratings_five_zero', 'ratings_zero_five',
                    'image', 'url', 'main', 'title', 'release_date', 'description']

    return df.drop(cols_to_drop, axis=1)


# CLEANING IN NOTEBOOK FUNCTION
# This function runs all the above functions on the dataframe version of the raw data
# The function also replaces plays of -1 with plays of 0
# It returns a cleaned dataframe
# Import functions at top of notebook with:
# from preprocessing.preprocess_1_cleaning import *

def cleaning_in_notebook(df):
    numeric_columns = ['plays','playing','backlogs','wishlist','total_reviews','total_lists']
    string_columns = ['developers','genres','platforms']
    df2 = drop_duplicates(df)
    df3 = drop_no_release_date(df2)
    df4 = change_to_datetype(df3, 'release_date')
    df4_5 = create_gen_3(df4)
    df4[string_columns] = make_list_columns_to_lists(df4_5, string_columns)
    for x in numeric_columns:
        numeric_objects_reformatted(df4, x)
    df4['plays'] = np.where(df4['plays'] < 0, 0, df4['plays'])


    return df4
