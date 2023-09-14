import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn import set_config; set_config(display='diagram')

sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *
from preprocessing.preprocess_2_features import *
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler

from sklearn.pipeline import make_pipeline
from sklearn.pipeline import make_union
from sklearn.compose import make_column_transformer
import datetime
from sklearn.preprocessing import MultiLabelBinarizer


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
    no_genre = concats.drop('genres', axis=1)
    no_gen = pd.get_dummies(no_genre, columns=['gen'])

    return no_gen


num_transformer = Pipeline([('mm_scaler', MinMaxScaler())])

col_transformer = ColumnTransformer([('num_transformer', num_transformer,
                                   ['plays','playing','backlogs','wishlist','total_reviews','total_lists'])],
                                  remainder='passthrough')

def make_training_data(reference_data):
    dropped = drop_unnecesary_coulumns(reference_data)

    transformed = pd.DataFrame(col_transformer.fit_transform(dropped))

    X_train = transformed.drop(6, axis=1)
    y_train = transformed[6]

    return X_train, y_train
