from __future__ import print_function
import base64
import json
import requests
import sys
import pprint
import sys
import spotipy    
import spotipy.util as util
import time  
import datetime
from random import shuffle 
from spotipy.oauth2 import SpotifyClientCredentials

# Workaround to support both python 2 & 3
try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']
USERNAME = CLIENT['username']

CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

if sys.version_info[0] >= 3:
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in list(auth_query_parameters.items())])
else: 
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in auth_query_parameters.items()])


AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)

def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    
    #python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
        headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    else: 
        base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
        headers = {"Authorization": "Basic {}".format(base64encoded)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header

GET_ARTIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'artists')  # /<id>

def get_artist(artist_id):
    url = "{}/{id}".format(GET_ARTIST_ENDPOINT, id=artist_id)
    resp = requests.get(url)
    return resp.json()

def get_several_artists(list_of_ids):
    url = "{}/?ids={ids}".format(GET_ARTIST_ENDPOINT, ids=','.join(list_of_ids))
    resp = requests.get(url)
    return resp.json()

def get_artists_albums(artist_id):
    url = "{}/{id}/albums".format(GET_ARTIST_ENDPOINT, id=artist_id)
    resp = requests.get(url)
    return resp.json()

def get_artists_top_tracks(artist_id, country='US'):
    url = "{}/{id}/top-tracks".format(GET_ARTIST_ENDPOINT, id=artist_id)
    myparams = {'country': country}
    resp = requests.get(url, params=myparams)
    return resp.json()

def get_related_artists(artist_id):
    url = "{}/{id}/related-artists".format(GET_ARTIST_ENDPOINT, id=artist_id)
    resp = requests.get(url)
    return resp.json()

SEARCH_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'search')

USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(
    USER_PROFILE_ENDPOINT, 'top')  # /<type>
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'recently-played')
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse',
                                              'featured-playlists')

def get_users_profile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_users_playlists(auth_header):
    url = USER_PLAYLISTS_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_users_top(auth_header, t):
    if t not in ['artists', 'tracks']:
        print('invalid type')
        return None
    url = "{}/{type}".format(USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT, type=t)
    resp = requests.get(url, headers=auth_header)
    print(resp)

def get_users_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_featured_playlists(auth_header):
    url = BROWSE_FEATURED_PLAYLISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()

GET_ALBUM_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'albums')  # /<id>

def get_album(album_id):
    url = "{}/{id}".format(GET_ALBUM_ENDPOINT, id=album_id)
    resp = requests.get(url)
    return resp.json()

def get_several_albums(list_of_ids):
    url = "{}/?ids={ids}".format(GET_ALBUM_ENDPOINT, ids=','.join(list_of_ids))
    resp = requests.get(url)
    return resp.json()

def get_albums_tracks(album_id):
    url = "{}/{id}/tracks".format(GET_ALBUM_ENDPOINT, id=album_id)
    resp = requests.get(url)
    return resp.json()

GET_USER_ENDPOINT = '{}/{}'.format(SPOTIFY_API_URL, 'users')

def get_user_profile(user_id):
    url = "{}/{id}".format(GET_USER_ENDPOINT, id=user_id)
    resp = requests.get(url)
    return resp.json()

GET_TRACK_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'tracks')  # /<id>

def get_track(track_id):
    url = "{}/{id}".format(GET_TRACK_ENDPOINT, id=track_id)
    resp = requests.get(url)
    return resp.json()

def get_several_tracks(list_of_ids):
    url = "{}/?ids={ids}".format(GET_TRACK_ENDPOINT, ids=','.join(list_of_ids))
    resp = requests.get(url)
    return resp.json()

