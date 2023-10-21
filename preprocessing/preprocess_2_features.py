import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import datetime

from sklearn.preprocessing import MultiLabelBinarizer, PowerTransformer
from sklearn.compose import ColumnTransformer

# ONE HOT ENCODER
def categorical_encoder(category):
    '''
    Creates an OHE, and returns the columns as well as the encoder
    '''
    mlb = MultiLabelBinarizer()
    transformed = mlb.fit_transform(category)

    df = pd.DataFrame(transformed, columns=mlb.classes_)

    return df, mlb

# This function needs to happen after the above
# It reduces the amount of OHE columns based on popularity
def keep_x_OHE_columns(OHE_coulmns, num_features=10):
    """
    Slices by the X (num_featutes) most common columns
    Returns only the amount specified
    """
    cols_by_power = pd.DataFrame(OHE_coulmns.sum().sort_values(ascending=False))

    top_X_columns = list(cols_by_power[0:num_features].index)
    cols_to_keep = OHE_coulmns[top_X_columns]

    return cols_to_keep


# This function does the same thing as the above one, but for multiple OHE categories
# It returns a df of only the top x ohe columns for each
# I recommend its used on Genre and Platform, but not Developer - not strict
def keeping_ohe_columns_and_dropping_the_originals(df_of_columns, num_ohe):
    """
    Returns a df of all categorical functions.
    Does not return the encoder.
    """
    empty = pd.DataFrame()

    columns = list(df_of_columns.columns)

    for col in columns:
        encoded_col, col_encoder = categorical_encoder(df_of_columns[col])
        cols_to_keep = keep_x_OHE_columns(encoded_col, num_ohe)
        empty = pd.concat((empty, cols_to_keep), axis=1)

    return empty


# CREATING GENERATIONAL FEATURE
# This function subsets the generation
def create_gen(seri):
    """
    Creates 5 generations based on time
    """
    gen_1_end = datetime.datetime.strptime('1983-01-01', '%Y-%m-%d')
    gen_2_end = datetime.datetime.strptime('1995-01-01', '%Y-%m-%d')
    gen_3_end = datetime.datetime.strptime('2006-01-01', '%Y-%m-%d')
    gen_4_end = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d')
    gen_5_end = datetime.datetime.strptime('2023-10-01', '%Y-%m-%d')

    dupe = seri
    dupe['gen'] = None

    for i, date in enumerate(dupe['release_date']):
        if date < gen_1_end:
            dupe.iloc[i, 27] = 1
        elif date < gen_2_end:
            dupe.iloc[i, 27] = 2
        elif date < gen_3_end:
            dupe.iloc[i, 27] = 3
        elif date < gen_4_end:
            dupe.iloc[i, 27] = 4
        elif date < gen_5_end:
            dupe.iloc[i, 27] = 5
        else:
            dupe.iloc[i, 27] = 6
    return dupe


def create_gen_3(seri):
    """
    Creates 3 generations based on time
    """
    gen_1_end = datetime.datetime.strptime('1983-01-01', '%Y-%m-%d')
    gen_2_end = datetime.datetime.strptime('1995-01-01', '%Y-%m-%d')
    gen_3_end = datetime.datetime.strptime('2006-01-01', '%Y-%m-%d')
    gen_4_end = datetime.datetime.strptime('2014-01-01', '%Y-%m-%d')
    gen_5_end = datetime.datetime.strptime('2023-10-01', '%Y-%m-%d')

    dupe = seri
    dupe['gen'] = None

    for i, date in enumerate(dupe['release_date']):
        if date < gen_2_end:
            dupe.iloc[i, 27] = 1
        elif date < gen_4_end:
            dupe.iloc[i, 27] = 2
        else:
            dupe.iloc[i, 27] = 3

    return dupe


def yeo_johnson_scaling(X_train, column):
    """
    This scales skewed data, and must be fed X_train and not the entire dataset
    Otherwise you looks visibility on your y, or just make it harder to find
    """
    num_transformer_yeo = PowerTransformer(method='yeo-johnson', standardize=False)

    col_transformer = ColumnTransformer([('num_transformer', num_transformer_yeo,
                                    [column])],
                                    remainder='passthrough')

    transfomed_X_train = pd.DataFrame(col_transformer.fit_transform(X_train))

    return transfomed_X_train

def drop_column_and_concat(data, new_columns, column_to_drop):
    new_df = pd.concat((data, new_columns), axis=1)
    new_df.drop(columns=column_to_drop, inplace=True)

    return new_df
