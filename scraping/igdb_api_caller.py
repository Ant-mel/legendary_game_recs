import os
import sys
import pandas as pd
import requests
from igdb.wrapper import IGDBWrapper
import json
sys.path.append("/Users/antonis/code/Ant-mel/legendary_game_recs/")
from flask import Flask
from processing_utils import process_raw_data
from scraping_and_api_utils import  prepare_json_df
from google.cloud import secretmanager


from google.cloud import bigquery


# Checks if a file exists. If the file exists then then this wont run
flag_file_path = "/app/flag_file.txt"

if os.path.exists(flag_file_path):
    print("Script has already been run. Exiting.")
    sys.exit(0)


# Create a Secret Manager client
secret_client = secretmanager.SecretManagerServiceClient()

# Define the name of the secret
secret_id_name = "projects/legendary-game-recs/secrets/CLIENT_ID/versions/latest"
secret_client_name = "projects/legendary-game-recs/secrets/CLIENT_SECRET/versions/latest"
secret_grant_name = "projects/legendary-game-recs/secrets/GRANT_TYPE/versions/latest"

# # Access the secret
secret_id_response = secret_client.access_secret_version(request={"name": secret_id_name})
secret_client_response = secret_client.access_secret_version(request={"name": secret_client_name})
secret_grant_response = secret_client.access_secret_version(request={"name": secret_grant_name})

# Credentials for calling the API
CLIENT_ID = secret_id_response.payload.data.decode("UTF-8")
CLIENT_SECRET = secret_client_response.payload.data.decode("UTF-8")
GRANT_TYPE = secret_grant_response.payload.data.decode("UTF-8")


# List of games used in the model
client = bigquery.Client()

query = f"""
        SELECT DISTINCT * FROM `legendary-game-recs.game_data_01_24.game_data`
        WHERE release_date != '0001-01-01T00:00:00' AND category = 'main' AND avg_review > 0

        UNION ALL

        SELECT DISTINCT * FROM `legendary-game-recs.game_data_01_24.game_data_test`
        WHERE release_date != '0001-01-01T00:00:00' AND category = 'main' AND avg_review > 0
    """

query_job = client.query(query)
results = query_job.result()
all_data = results.to_dataframe()

list_of_game_id = all_data['game_id']


#Generating the access token
response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}')
response_json = response.json()
ACCESS_TOKEN = response_json['access_token']


#This is a wrapper from IGDB just for their API
wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

no_data = []
list_sons = []
count = 0

for game in list_of_game_id:
    count += 1

    try:
        the_feat = json.loads(wrapper.api_request('games',
                f'fields franchise, franchises, storyline, aggregated_rating,aggregated_rating_count, game_engines.name, game_modes.name, multiplayer_modes, player_perspectives.name, themes.name, rating; where id = {int(game)};'))
        list_sons.append(the_feat[0])
        print(f'Success at {count}')

    except:
        print(f'failed at {count}')
        no_data.append(game)

missed = pd.DataFrame(no_data, columns=['game_id'])
new_df = prepare_json_df(pd.DataFrame(list_sons))

everything = all_data.merge(new_df, right_on='id', left_on='game_id', how='right')

# You need to ensure the categorical columns can go in as strings
# Because BiqQuery treats it like a JSON
list_of_lists = ['game_modes', 'franchises', 'franchise', 'player_perspectives', 'themes', 'multiplayer_modes', 'game_engines']
everything[list_of_lists] = everything[list_of_lists].astype(str)

#Uploads all data to the cloud
job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
job = client.load_table_from_dataframe(everything, 'legendary-game-recs.game_data_01_24.all_data', job_config=job_config)

#Uploads Missed data to the cloud
job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
job = client.load_table_from_dataframe(missed, 'legendary-game-recs.game_data_01_24.igdb_missed_data', job_config=job_config)


# Makes the script shutdown
with open(flag_file_path, "w") as flag_file:
    flag_file.write("Script has been run")
