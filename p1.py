import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict

"""
load_user_playlists FUNCTION
"""
def load_user_playlists(user_id):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlists = sp.user_playlists(user_id)
    playlists_all = playlists['items']
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            # print(playlist['id'])
            # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            continue
        if playlists['next']:
            playlists = sp.next(playlists)
            playlists_all.extend(playlists['items'])
        else:
            playlists = None

    return playlists_all

"""
load_playlist_songs FUNCTION
"""
def load_playlist_songs(playlist_id):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    tracks = []
    result = sp.playlist_items(playlist_id, additional_types=['track'])
    tracks.extend(result['items'])

    # if playlist is larger than 100 songs, continue loading it until end
    while result['next']:
        result = sp.next(result)
        tracks.extend(result['items'])

    return tracks

"""
collate_songs_from_playlists FUNCTION
"""
def collate_songs_from_playlists(playlists):
    songs = defaultdict(list)

    for playlist in playlists:
        playlist_songs = load_playlist_songs(playlist['id'])

        for song in playlist_songs:
            if not song['track']: # TODO FOR PODCAST TRACKS
                song_name = "PODCAST"
                song_id = ""
                print(song)
            else:
                # print(song['track']['name'])
                # print(song['track']['id'])
                song_name = song['track']['name']
                song_id = song['track']['id']

                if not song['track']['id']:
                    song_id = "LOCAL"

            songs[song_name + " | " + song_id].append(playlist['name'])
    
    return songs

# GET PRELIMINARY DATA
user_id = '22yxrpnqslh2ch2s2ls32irwy'
my_playlists = load_user_playlists(user_id)
songs = collate_songs_from_playlists(my_playlists)

# WRITE SONGS DEFAULTDICT TO JSON
with open('myfile.json', 'w', encoding ='utf8') as json_file:
    json.dump(songs, json_file, ensure_ascii = True)

# EXTRACT ANALYTICS FROM SONGS DATA TODO
num_playlists = str(len(my_playlists))

non_track_entries = str(len(songs["PODCAST"]))

total_songs = str(len(songs)) # may be off by 1 due to podcast entry

duplicate_songs = defaultdict(list)

for key in songs.keys():
    if len(songs[key]) > 1 and key != "PODCAST":
        duplicate_songs[key].append(songs[key])

# WRITE ANALYTICS TO OUTPUT TEXT FILE
with open('results.txt', 'w', encoding ='utf8') as f:
    f.write('Number of playlists: ' + num_playlists + '\n')
    f.write('Number of non-track entries: ' + non_track_entries + '\n')
    f.write('Total songs: ' + total_songs + '\n')
    
    f.write('\n' + 'Songs Duplicated Across Playlists:' + '\n')

    for dup in duplicate_songs.items():
        song = dup[0]
        dup_playlists = dup[1][0]
        print(song)
        print(dup_playlists)

        f.write(song + '\n')
        for playlist in dup_playlists:
            f.write('\t' + playlist + '\n')
