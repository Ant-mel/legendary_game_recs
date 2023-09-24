import pandas as pd
import sys
sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from preprocessing.preprocess_1_cleaning import *


def genre_filter(df, selected_genres):
    if len(selected_genres) == 0:
        return df

    if selected_genres == ['Any']:
        pass
    else:
        if len(selected_genres) == 1:
            df_filt = df[df['genres'].apply(lambda x:
                selected_genres[0] in x)]
            return df_filt
        if len(selected_genres) == 2:
            df_filt = df[df['genres'].apply(lambda x:
                selected_genres[0] in x or
                selected_genres[1] in x)]
            return df_filt
        if len(selected_genres) == 3:
            df_filt = df[df['genres'].apply(lambda x:
                selected_genres[0] in x or
                selected_genres[1] in x or
                selected_genres[2] in x)]
            return df_filt
        if len(selected_genres) == 4:
            df_filt = df[df['genres'].apply(lambda x:
                selected_genres[0] in x or
                selected_genres[1] in x or
                selected_genres[2] in x or
                selected_genres[3] in x)]
            return df_filt
        if len(selected_genres) == 5:
            df_filt = df[df['genres'].apply(lambda x:
                selected_genres[0] in x or
                selected_genres[1] in x or
                selected_genres[2] in x or
                selected_genres[3] in x or
                selected_genres[4] in x)]
            return df_filt


def platform_filter(df, selected_platforms):
    if len(selected_platforms) == 0:
        return df

    if selected_platforms == ['Any']:
        return df
    else:
        if len(selected_platforms) == 1:
            df_filt = df[df['platforms'].apply(lambda x:
                selected_platforms[0] in x)]
            return df_filt
        if len(selected_platforms) == 2:
            df_filt = df[df['platforms'].apply(lambda x:
                selected_platforms[0] in x or
                selected_platforms[1] in x)]
            return df_filt
        if len(selected_platforms) == 3:
            df_filt = df[df['platforms'].apply(lambda x:
                selected_platforms[0] in x or
                selected_platforms[1] in x or
                selected_platforms[2] in x)]
            return df_filt
        if len(selected_platforms) == 4:
            df_filt = df[df['platforms'].apply(lambda x:
                selected_platforms[0] in x or
                selected_platforms[1] in x or
                selected_platforms[2] in x or
                selected_platforms[3] in x)]
            return df_filt
        if len(selected_platforms) == 5:
            df_filt = df[df['platforms'].apply(lambda x:
                selected_platforms[0] in x or
                selected_platforms[1] in x or
                selected_platforms[2] in x or
                selected_platforms[3] in x or
                selected_platforms[4] in x)]
            return df_filt


def time_range_start_stop(df, start, stop):
    zone_1 = pd.Timestamp(datetime.datetime.strptime('1980-01-01', '%Y-%m-%d'))
    zone_2 = pd.Timestamp(datetime.datetime.strptime('1990-01-01', '%Y-%m-%d'))
    zone_3 = pd.Timestamp(datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
    zone_4 = pd.Timestamp(datetime.datetime.strptime('2010-01-01', '%Y-%m-%d'))
    zone_5 = pd.Timestamp(datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'))
    today_date = pd.Timestamp(datetime.date.today())



    if start == 'Any':
        df_filt_start = df
    if start == 'Prehistoric':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    zone_1 > x)]
    if start == '1980s':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    zone_2 < x)]
    if start == '1990s':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    zone_3 < x)]
    if start == '2000s':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    zone_4 < x)]
    if start == '2010s':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    zone_5 < x)]
    if start == '2020s':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    today_date < x)]
    if start == 'Upcoming':
        df_filt_start = df[df['release_date'].apply(lambda x:
                    today_date > x)]

    if stop == 'Any':
        return df_filt_start
    if stop == 'Prehistoric':
        df_filt_end = df_filt_start[df_filt_start['release_date'].apply(lambda x:
                    zone_1 > x)]
    if stop == '1980s':
        df_filt_end = df_filt_start[df_filt_start['release_date'].apply(lambda x:
                    zone_2 > x)]
        return df_filt_end
    if stop == '1990s':
        df_filt_end = df_filt_start[df_filt_start['release_date'].apply(lambda x:
                    zone_3 > x)]
        return df_filt_end
    if stop == '2000s':
        df_filt_end = df_filt_start[df_filt_start['release_date'].apply(lambda x:
                    zone_4 > x)]
        return df_filt_end
    if stop == '2010s':
        df_filt_end = df_filt_start[df_filt_start['release_date'].apply(lambda x:
                    zone_5 > x)]
        return df_filt_end
    if stop == '2020s':
        df_filt_end = df_filt_start[df_filt_start['release_date'].apply(lambda x:
                    today_date > x)]
        return df_filt_end
    if stop == 'Upcoming':
        return df_filt_start
