import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, PowerTransformer
from sklearn import set_config; set_config(display='diagram')

sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *
from preprocessing.preprocess_2_features import *
from preprocessing.preprocess_3_nlp import *
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler


# CLEANING PIPELINE & REFERENCE DATAFRAME

cleaning = FunctionTransformer(cleaning_in_notebook)
remove_0_reviews = FunctionTransformer(remove_no_reviews)
only_mains = FunctionTransformer(only_main_games)
drop_some_cols = FunctionTransformer(drop_unnecesary_coulumns)

pipeline = Pipeline([('cleaning', cleaning),
                     ('remove_no_reviews', remove_0_reviews),
                     ('keeps_only_main_games', only_mains)])

def pipeline_genre_ohe_only(df):
    '''
    This cleans the data, removes 0 value reviews and returns x amount of ohe columns of genre
    '''
    new_data = pipeline.fit_transform(df)
    reset_index_df = new_data.reset_index(drop=True)

    ohe, mlb = categorical_encoder(reset_index_df['genres'])
    cols = keep_x_OHE_columns(ohe)

    concats = pd.concat([reset_index_df, cols], axis=1)
    # no_genre = concats.drop('genres', axis=1)
    no_gen = pd.get_dummies(concats, columns=['gen'])

    return no_gen

def make_reference_df_full_csv(df):
    string_columns = ['developers','genres','platforms']
    df[string_columns] = make_list_columns_to_lists(df, string_columns)
    return df


# JOINING DESCRIPTION NLP TOPICS TO REFERENCE TO CREATE MODEL DF
def make_model_df(df1, df2):
    '''
    Takes the reference df and the topics df and concatenate
    '''
    return pd.concat((df1, df2), axis=1)

# TRAINING DATA PIPELINE

num_transformer = Pipeline([('mm_scaler', MinMaxScaler())])

col_transformer = ColumnTransformer([('num_transformer', num_transformer,
                                    ['plays','playing','backlogs','wishlist','total_reviews','total_lists'])],
                                    remainder='passthrough')

def make_training_data(reference_data):
    """
    Uses MinMax Scaler to create training data
    Returns X_train and y_train
    """
    no_genre = reference_data.drop('genres', axis=1)
    dropped = drop_unnecesary_coulumns(no_genre)

    transformed = pd.DataFrame(col_transformer.fit_transform(dropped))

    X_train = transformed.drop(6, axis=1)
    y_train = transformed[6]

    return X_train, y_train


num_transformer_yeo = PowerTransformer(method='yeo-johnson', standardize=False)

col_transformer_yeo = ColumnTransformer([('num_transformer', num_transformer_yeo,
                                   ['plays','playing','backlogs','wishlist','total_reviews','total_lists'])],
                                  remainder='passthrough')

def make_training_data_yeo(reference_data):
    """
    Uses Yeo-Johnson scaling to create training data
    Returns X_train and y_train
    """
    no_genre = reference_data.drop('genres', axis=1)
    dropped = drop_unnecesary_coulumns(no_genre)

    transformed = pd.DataFrame(col_transformer_yeo.fit_transform(dropped))

    X_train = transformed.drop(6, axis=1)
    y_train = transformed[6]

    return X_train, y_train


def ohe_and_nlp(data, ohe_column_name, n_ohe_features, nlp_column_name, n_nlp_features):
    """
    Creates both OHE and NLP features
    """
    ohe_columns = keeping_ohe_columns_and_dropping_the_originals(data[[ohe_column_name]], n_ohe_features)

    ohe_added_to_data = drop_column_and_concat(data, ohe_columns, ohe_column_name)

    ohe_and_topics = topics_from_nlp(ohe_added_to_data, nlp_column_name, n_nlp_features)

    return ohe_and_topics
