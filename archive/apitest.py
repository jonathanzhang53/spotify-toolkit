import requests
import sys

CLIENT_ID = "b38ca4ba21994e978786f16b70bce288"
CLIENT_SECRET = "4fb5268d4aa7466ebf78f2ea9fca867f"
USER_ID = "22yxrpnqslh2ch2s2ls32irwy"

AUTH_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/"

# retrieving access token
auth_response = requests.post(AUTH_URL, {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

headers = {
    "Authorization": "Bearer {token}".format(token=access_token)
}

# EXAMPLE CODE: searching data for a song 
track_id = "5CalS8Gn69OOrR9aiw0ZO9"
r = requests.get(BASE_URL + "audio-features/" + track_id, headers=headers)
r = r.json()
# print(r)

# get playlists: https://developer.spotify.com/console/get-playlists/
# need to implement offset to get more than 50 playlists
r = requests.get(BASE_URL + "users/" + USER_ID + "/playlists?limit=50", headers=headers)
r = r.json()
# print(r)
print("Number of playlists: " + str(len(r["items"])))
for playlist in r["items"]:
    print(playlist["name"])