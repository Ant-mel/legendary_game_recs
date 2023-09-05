import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import datetime

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

# NUMERIC PROCESSING

# The below functions clean Plays, Playing, Backlogs, Wishlist,
# Total_Reviews, Total_Lists columns
# Only the last function matters - numeric_objects_reformatted
# It runs all the ones above it

def remove_K_and_fullstop(x):
    '''This function removes the K and . from objects such as 4.1K, replacing with 4100'''
    if 'K' in x and '.' in x:
        x = x.replace('K', '00')
        x = x.replace('.','')
        return x
    else:
        return x

def remove_K(x):
    '''This function removes the K from objscts such as 92K, replacing with 92000'''
    if 'K' in x:
        return x.replace('K','000')
    else:
        return x

#This is the final function for use on numeric columns
# numeric_columns = ['plays','playing','backlogs','wishlist','total_reviews','total_lists']
def numeric_objects_reformatted(df, column):
    '''This function applies the removal of K and . above in order, and returns as integers'''
    df[column] = df[column].apply(remove_K_and_fullstop)
    df[column] = df[column].apply(remove_K)
    df[column] = df[column].astype('int')
    return df


# DATE PROCESSING

#The below functions clean the Release_Date column
# Only the last function matters - date_reformatted
# It runs all the ones above it

def remove_hyphens(x):
    '''This function removes hyphens between numbers'''
    if '-' in x:
        x = x.replace('-', '')
        return str(x)

def change_to_datetype(x):
    '''This function changes objects to null if no date, or date type'''
    if x == '00010101':
        return 'null'
    else:
        return datetime.strptime(x, '%Y%m%d').strftime('%m/%d/%Y')


#This is the final function for use on date columns
def date_reformatted(df, column):
    '''This function applies the functions above to return a date type column'''
    df[column] = df[column].apply(remove_hyphens)
    df[column] = df[column].apply(change_to_datetype)
    return df

# ONE HOT ENCODER
def categorical_encoder(category):
    '''This creates an OHE, and returns the columns as well as the encoder'''
    mlb = MultiLabelBinarizer()
    transformed = mlb.fit_transform(category)

    df = pd.DataFrame(transformed, columns=mlb.classes_)

    return df, mlb

# This function needs to happen after the above
# It reduces the amount of OHE columns based on popularity
def keep_x_OHE_columns(OHE_coulmns, num_features=10):
    """Slices by the X (num_featutes) most common columns"""
    """Returns only the amount specified"""
    cols_by_power = pd.DataFrame(OHE_coulmns.sum().sort_values(ascending=False))

    top_20_OHE = list(cols_by_power[0:num_features].index)
    cols_to_keep = OHE_coulmns[top_20_OHE]

    return cols_to_keep


# This function does the same thing as the above one, but for multiple OHE categories
# It returns a df of only the top x ohe columns for each
# I recommend its used on Genre and Platform, but not Developer - not strict
def keeping_ohe_columns_and_dropping_the_originals(df_of_columns, num_ohe):
    """Returns a df of all categorical functions, but does not return the encoder.
    I will need to find out the best way to return the encoder for processing new data
    """
    empty = pd.DataFrame()

    columns = list(df_of_columns.columns)

    for col in columns:
        encoded_col, col_encoder = categorical_encoder(df_of_columns[col])
        cols_to_keep = keep_x_OHE_columns(encoded_col, num_ohe)
        empty = pd.concat((empty, cols_to_keep), axis=1)

    return empty
