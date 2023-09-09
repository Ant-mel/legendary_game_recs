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

# data = pd.read_csv("../raw_data/all_game_data_v1_corrected2.csv", low_memory=False)

def preproc(game_title_df):
    input_data = pd.read_csv("../raw_data/all_game_data_v1_corrected2.csv", low_memory=False)

    cleaning_transformer = FunctionTransformer(cleaning_in_notebook)
    no_reviews_transformer = FunctionTransformer(remove_no_reviews)
    cleaning_pipeline = Pipeline([('cleaning', cleaning_transformer),
                        ('no_review', no_reviews_transformer)])

    df = cleaning_pipeline.fit_transform(input_data)
    test_df = df[['avg_review','plays','playing','backlogs','wishlist','total_reviews','total_lists']]

    num_transformer = Pipeline([('imputer', SimpleImputer(strategy="median")),
                             ('mm_scaler', MinMaxScaler())
                            ])

    preprocessor = ColumnTransformer([('num_transformer', num_transformer,
                                   ['plays','playing','backlogs','wishlist','total_reviews','total_lists'])],
                                  remainder='passthrough')

    # knn_model = KNeighborsRegressor(n_neighbors=11)
    # model_pipeline = make_pipeline(preprocessor, knn_model)

    X_train = test_df[['plays','playing','backlogs','wishlist','total_reviews','total_lists']]
    y_train = test_df['avg_review']

    X_train_scaled = preprocessor.fit_transform(X_train)

    #Model
    knn_model = KNeighborsRegressor(n_neighbors=11).fit(X_train_scaled, y_train)

    X_new = game_title_df[['plays','playing','backlogs','wishlist','total_reviews','total_lists']]
    X_new_scaled = preprocessor.fit_transform(X_new)

    result = knn_model.kneighbors(X_new_scaled,n_neighbors=11)

    # Pass song to model, ask for 11 closest points, and unpack the corresponding indices to a list
    ind_list = list(result[1][0])

# Filter original dataframe with indices list and sort by tempo
    df.iloc[ind_list, :].sort_values(by="avg_review")


    return df.iloc[ind_list, :].sort_values(by="avg_review")
