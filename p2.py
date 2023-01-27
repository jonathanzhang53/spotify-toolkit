import json
from collections import defaultdict

### LOAD FROM JSON
with open('songs.json', 'r') as f:
    songs = json.load(f)
with open('playlists.json', 'r') as f:
    playlists = json.load(f)

### CONVERT TO songs DEFAULTDICT
print(songs)
# print(playlists)

# EXTRACT ANALYTICS FROM SONGS DATA TODO
num_playlists = str(len(playlists))

non_track_entries = str(len(songs['PODCAST | ']))

total_songs = str(len(songs)) # may be off by 1 due to podcast entry

duplicate_songs = defaultdict(list)

for key in songs.keys():
    if len(songs[key]) > 1 and key != 'PODCAST | ':
        duplicate_songs[key].append(songs[key])

# WRITE ANALYTICS TO OUTPUT TEXT FILE
with open('results/results.txt', 'w', encoding ='utf8') as f:
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
