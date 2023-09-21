import sys
sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
import streamlit as st
from streamlit_searchbox import st_searchbox
from preprocessing.pipeline_the_unification import *
from preprocessing.api_processing import *
from model.model_create import *
from igdb.wrapper import IGDBWrapper
import requests
import os
import json
import pandas as pd
import pickle
from PIL import Image
from io import BytesIO
import datetime


st.write('WELCOME BITCHES')

# Specify the path to the file containing game titles
games = pd.read_csv('raw_data/reference_csv_v1')
X_train = pd.read_csv('raw_data/basline_X_train')
model = pickle.load(open('model/basline_model', 'rb'))

# Create a search input for filtering games
# search_query = st.text_input("Type the title of a game:")

# Initialize a list to store filtered game titles
filtered_games = []

# Function to update the recommendation list
def update_recommendations(query):
    filtered_games.clear()
    if len(query) >= 1:
        for game in games:
            if query.lower() in game.lower():
                filtered_games.append(game)

# Display the filtered game titles
st.write("Recommendations:")

# if search_query:
# update_recommendations(search_query)
# if filtered_games:
selected_game = st.selectbox("Select a game:", games)

if selected_game:
    st.write(f"You selected: {selected_game}")

    # Chosen game variables
    df_row = games[games['title'] == selected_game]
    index = df_row.index[0]


    #Making a prediction
    list_of_predictions = predict_baseline_model(index, model, games, X_train)
    first_rec_game_id = int(list_of_predictions[1:2]['game_id'])

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
                f'fields cover.url, cover.image_id, name, release_dates.date, genres.name, videos.video_id; where id = {first_rec_game_id};'))

    # st.write(str(list_of_predictions[1:2]['genres']))
    st.write(the_feat[0]['videos'][0]['video_id'])

    # DATA TO SHOW
    '''Cover image'''
    image_id = str(the_feat[0]['cover']['image_id'])
    second_url = f'https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg'

    '''Name'''
    name = the_feat[0]['name']

    '''Date'''
    unix_time = the_feat[0]['release_dates'][0]['date']
    normal_date = str(datetime.datetime.utcfromtimestamp(unix_time))[:10]

    '''Genres'''
    genre_list = str(get_names_from_dict(the_feat[0]['genres']))[1:-1].replace("'", '')

    '''video'''
    youtube_base = 'https://www.youtube.com/watch?v='
    # game_video_id = the_feat[0]['videos'][0]['video_id'][0]
    # video_file = open(youtube_base + game_video_id)

    st.title(f'You should try:')

    col1, col2 = st.columns(2)

    with col1:
        st.image(second_url)

    with col2:
        st.write(name)
        st.write(normal_date)
        st.write(genre_list)
        st.video()






    # response_img = requests.get("http:" + url)
    # img = Image.open(BytesIO(response.content))
    # st.image(img)
