import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

# registering client credentials
client_credentials_manager = SpotifyClientCredentials(client_id='b0a9a9fab5f34b079bf01c6525740dc8',
                                                           client_secret='e094da5c46f24cda9d038fb68db6670e')
# creating object to call methods from the library
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create a dictionary of albums
albums = spotify.artist_albums('spotify:artist:3mIj9lX2MWuHmhNCA7LSCW', album_type='album')
album_dict = {}
for album in albums['items']:
	# do not add if live version
	if (album['name'].find('Live') > -1):
		continue
	else:
		# put albums and corresponding uri into a dictionary
		album_dict[album['name']] = album['uri']

# create a dictionary of track ids
track_id_dict = {}
for album_id in album_dict.keys():
	tracks = spotify.album_tracks(album_dict[album_id])
	for track in tracks['items']:
		# do not add if remix
		if (track['name'].find('Remix') > -1):
			continue
		else:
			track_id_dict[track['name']] = track['uri']

# create a dictionary of track: audio features
audio_features_dict = {}
for track in track_id_dict:

	audio_features_dict[track] = spotify.audio_features(track_id_dict[track])[0]

audio_features_dict[spotify.track('spotify:track:2i1CnSeLjppv41BTuc7qhY')['name']] = spotify.audio_features('spotify:track:2i1CnSeLjppv41BTuc7qhY')[0]
# simplify the audio features dictionary to make it able to put into pandas data frame

for track in audio_features_dict:
	column_names = audio_features_dict[track].keys()
	audio_features_dict[track] = audio_features_dict[track].values()

data = pd.DataFrame.from_dict(audio_features_dict, orient= 'index', columns= column_names)
data.to_csv('data.csv', index=True)


##### similarity calculations #####

def similarity_calculator(feature, track):
	# percentage error
	return (abs(data.loc[track, feature] - data.loc["Frail State Of Mind", feature]) / data.loc["Frail State Of Mind", feature])

# create a new dictionary that holds track name: similarity
similarity_dict = {}
# iterate through all original tracks
for track in track_id_dict:
	# reset the similarity value for each track
	value = 0
	for feature in column_names:
		# calculated the similarity for each column if it is a numerical value
		if type(data.loc[track, feature]) != str: 
			value += similarity_calculator(feature, track)
		else:
			break
	# add track and value into the new dictionary
	similarity_dict[track] = value

# sort the dictionary by values in ascending order
sorted_dict = sorted(similarity_dict, key=similarity_dict.__getitem__)
print(sorted_dict)

