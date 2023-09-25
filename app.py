import sys
import os

# sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")

# Was hoping to put the site online...
script_directory = os.path.dirname(os.path.abspath(__file__))
# Add the project root directory to sys.path
project_root_directory = os.path.join(script_directory, '..')
sys.path.append(project_root_directory)

import streamlit as st
from preprocessing.pipeline_the_unification import change_to_datetype
from preprocessing.api_processing import get_names_from_dict
from model.model_create import predict_baseline_model
from front_end.app_filters import genre_filter, time_range_start_stop, platform_filter
from igdb.wrapper import IGDBWrapper
import requests
import json
import pandas as pd
import datetime
from joblib import load


st.title("World's best video game recommendation engine")

# Specify the path to the file containing game titles
# raw_reference = pd.read_csv('raw_data/reference_csv_v1')
# raw_reference[['genres', 'platforms']] = make_list_columns_to_lists(raw_reference, ['genres', 'platforms'])
# raw_data_date = change_to_datetype(raw_reference, 'release_date')

# This is for running the app online
raw_data = pd.read_json('data/reference_df_v3', orient='records', lines=True)
games = change_to_datetype(raw_data, 'release_date')
X_train = pd.read_json('data/xtrain_df_v3', orient='records', lines=True)
model = load('model/model_v3.joblib')


# This is fro running the app locally
# raw_data = pd.read_json('raw_data/reference_df_v3', orient='records', lines=True)
# games = change_to_datetype(raw_data, 'release_date')
# X_train = pd.read_json('raw_data/xtrain_df_v3', orient='records', lines=True)
# model = load('raw_data/model_v3.joblib')


# Initialize a list to store filtered game titles
filtered_games = []

# Function to update the recommendation list
def update_recommendations(query):
    filtered_games.clear()
    if len(query) >= 1:
        for game in games:
            if query.lower() in game.lower():
                filtered_games.append(game)


list_of_genres = ['Any', 'Adventure', 'Arcade', 'Brawler', 'Card & Board Game', 'Fighting',
       'Indie', 'MOBA', 'Music', 'Pinball', 'Platform', 'Point-and-Click',
       'Puzzle', 'Quiz/Trivia', 'RPG', 'Racing', 'Real Time Strategy',
       'Shooter', 'Simulator', 'Sport', 'Strategy', 'Tactical',
       'Turn Based Strategy', 'Visual Novel']
list_of_times = ['Any', 'Prehistoric', '1980s', '1990s', '2000s', '2010s', '2020s', 'Upcoming']
list_of_consoles = ['Any','Windows PC', 'Mac', 'PlayStation 4', 'Nintendo Switch', 'Xbox One',
       'Linux', 'iOS', 'Android', 'PlayStation 3', 'PlayStation 2', 'Xbox 360',
       'Arcade', 'Web browser', 'Wii', 'PlayStation', 'PlayStation 5',
       'Nintendo DS', 'Xbox Series', 'PlayStation Portable', 'PlayStation Vita', 'Nintendo 3DS', 'Xbox', 'Wii U',
       'Sega Mega Drive/Genesis', 'NES', 'Game Boy Advance', 'SNES',
       'Nintendo GameCube', 'Amiga']

# Display the filtered game titles
# if search_query:
# update_recommendations(search_query)
# if filtered_games:
top_col1, top_col2 = st.columns(2)

with top_col1:
    selected_game = st.selectbox("Select a game:", games, placeholder='Select a game')

with top_col2:
    genre_box = st.multiselect('Select Genres', options=list_of_genres)

filt_col1, filt_col2 = st.columns(2)

with filt_col1:
    st.write('Select a time range')
    time_col1, time_col2 = st.columns(2)
    with time_col1:
        start_range = st.selectbox('Start', list_of_times)
    with time_col2:
        end_range = st.selectbox('End', list_of_times)
with filt_col2:
    st.write('Select Platforms')
    console = st.multiselect('', list_of_consoles)



if selected_game:
    # Chosen game variables
    df_row = games[games['title'] == selected_game]
    index = df_row.index[0]


    #Making a prediction
    list_of_predictions = predict_baseline_model(index, model, games, X_train)
    # Filtering the predicitons
    filt_genres = genre_filter(list_of_predictions, genre_box)
    filt_date = time_range_start_stop(filt_genres, start_range, end_range)
    filt_platform = platform_filter(filt_date, console)

    # st.write(int(filt_platform[1:2]['game_id']))

    first_rec_game_id = int(filt_platform[1:2]['game_id'])

    #Calling hte API
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    GRANT_TYPE = os.getenv("GRANT_TYPE")

    #Generating the access token
    response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}')
    response_json = response.json()
    ACCESS_TOKEN = response_json['access_token']

    #This is a wrapper from IGDB just for their API
    wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

    the_feat = json.loads(wrapper.api_request('games',
                f'fields cover.url, cover.image_id, name, release_dates.date, genres.name, summary, videos.video_id; where id = {first_rec_game_id};'))

    # st.write(the_feat[0]['summary'])

    # DATA TO SHOW
    image_id = str(the_feat[0]['cover']['image_id'])
    second_url = f'https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg'

    # Name
    name = the_feat[0]['name']

    # Summary
    summary = the_feat[0]['summary']

    #Time
    unix_time = the_feat[0]['release_dates'][0]['date']
    normal_date = str(datetime.datetime.utcfromtimestamp(unix_time))[:10]

    #Genres
    try:
        genre_list = str(get_names_from_dict(the_feat[0]['genres']))[1:-1].replace("'", '')
    except:
        genre_list = 'None'

    #Youtube Video
    youtube_base = 'https://www.youtube.com/watch?v='

    st.header('You should try:', divider='rainbow')

    # Setting up the columns
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(second_url)

    with col2:
        st.subheader(name)
        st.write(summary)

        st.markdown(f"**Released on**: {normal_date}")
        st.markdown(f'**Genres**: {genre_list}')


    try:
        game_video_id = str(the_feat[0]['videos'][0]['video_id'])
        video_file = youtube_base + game_video_id
        with st.expander(f"Watch trailer"):
            if video_file == None:
                pass
            else:
                st.video(video_file)
    except:
       pass
