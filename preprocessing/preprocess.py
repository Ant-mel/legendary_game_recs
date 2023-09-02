import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

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
def make_list_columns_to_lists(df, columns):
    '''This returns a dataframe of columns where lists where imported as strings, and returns them to their list state'''
    cleaned_df = pd.DataFrame()

    for col in columns:
        cleaned = clean_stringlists(df[col])
        cleaned_df[col] = cleaned
    return cleaned_df


# ONE HOT ENCODER
def categorical_encoder(category):
    '''This creates an OHE, and returns the columns as well as the encoder'''
    mlb = MultiLabelBinarizer()
    transformed = mlb.fit_transform(category)

    df = pd.DataFrame(transformed, columns=mlb.classes_)

    return df, mlb
