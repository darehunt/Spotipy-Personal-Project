import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# registering client credentials
client_credentials_manager = SpotifyClientCredentials(client_id='b0a9a9fab5f34b079bf01c6525740dc8',
                                                           client_secret='e094da5c46f24cda9d038fb68db6670e')
# creating object to call methods from the library
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# post malone id to get info
post_malone_uri = 'spotify:artist:246dkjvS1zLTtiykXe5h60'

# dict of artist information
artist = spotify.artist(post_malone_uri)
print(artist['name'])

# dict of top tracks
top_tracks = spotify.artist_top_tracks(post_malone_uri)
# top 10 tracks(values) from dictionary with key 'tracks'
for track in top_tracks['tracks'][:10]:
    track['name']

# dict of albums featuring artist
albums = spotify.artist_albums(post_malone_uri, album_type='album')
album_dict = {}
for album in albums['items']:
	# puts albums and corresponding uri into a dictionary
	album_dict[album['name']] = album['uri']

# creating a dictionary of track ids
track_id_dict = {}
for album_id in album_dict.keys():
	tracks = spotify.album_tracks(album_dict[album_id])
	for track in tracks['items']:
		track_id_dict[track['name']] = track['uri']

# print audio analyses for each track
for track in track_id_dict:
	print(track)
	audio_analysis = spotify.audio_analysis(track_id_dict[track])
