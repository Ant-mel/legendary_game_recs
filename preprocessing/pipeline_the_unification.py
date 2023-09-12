import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn import set_config; set_config(display='diagram')

sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *
from preprocessing.preprocess_2_features import *
from sklearn.compose import ColumnTransformer

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
                     ('keeps_only_main_games', only_mains),
                     ('drops_useless_columns', drop_some_cols)])


def pipeline_genre_ohe_only(df):
    '''
    This cleans the data, removes 0 value reviews and returns x amount of ohe columns of genre
    '''
    new_data = pipeline.fit_transform(df)
    reset_index = new_data.reset_index()

    ohe, mlb = categorical_encoder(reset_index['genres'])
    cols = keep_x_OHE_columns(ohe)

    concats = pd.concat([reset_index, cols], axis=1)

    return pd.get_dummies(concats, columns=['gen'])
