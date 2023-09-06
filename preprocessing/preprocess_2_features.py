import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import datetime

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
