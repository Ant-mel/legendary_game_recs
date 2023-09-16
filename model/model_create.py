import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import datetime
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

from sklearn.pipeline import make_pipeline
from sklearn.pipeline import make_union
from sklearn.compose import make_column_transformer

import sys
sys.path.append("/home/kieran/code/Ant-mel/legendary_game_recs/")

from preprocessing.preprocess_1_cleaning import *
from preprocessing.preprocess_2_features import *
from preprocessing.pipeline_the_unification import *



def create_baseline_model(raw_data):
    reference_data = pipeline_genre_ohe_only(raw_data)

    X_train, y_train = make_training_data(reference_data)

    knn_model = KNeighborsRegressor(
        n_neighbors=11).fit(X_train, y_train)

    return knn_model, reference_data, X_train

def predict_baseline_model(indicies, model, reference_data, X_train):
    game = X_train[indicies:indicies+1]

    ind_list = list(model.kneighbors(game,n_neighbors=11)[1][0])
    prediction = reference_data.iloc[ind_list]

    return prediction
