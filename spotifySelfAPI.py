import base64
import requests
from urllib.parse import urlencode

def SpotifyAuthAccessToken(s_client_id, s_client_secret, s_refresh_token):
  
    s_client_creds = f"{s_client_id}:{s_client_secret}"
    s_client_creds_b64 = base64.b64encode(s_client_creds.encode())
    
    s_token_headers = {
      "Authorization" : f"Basic {s_client_creds_b64.decode()}"
    }

    s_token_url = "https://accounts.spotify.com/api/token"

    s_token_data_refresh = {
      "grant_type" : "refresh_token",
      "refresh_token" : s_refresh_token
    }

    r = requests.post(s_token_url, data=s_token_data_refresh, headers = s_token_headers)
    
    if r.status_code in range(200, 299):
        s_token_response_data = r.json()
        return s_token_response_data['access_token']

def SpotifyPlaylistCreate(s_playlist_name, s_access_token):
    endpoint = "https://api.spotify.com/v1/users/r4xa4j5m4mjpz14d0kz0v9gfz/playlists"

    s_playlist_headers = {
        "Authorization" : f"Bearer {s_access_token}",
        "Content-Type" : "application/json"
    }

    s_playlist_data = {
        "name" : s_playlist_name,
        "public" : "false",
        "description" : "TPWK :)"
    }

    r = requests.post(endpoint, json=s_playlist_data, headers=s_playlist_headers)
    if r.status_code in range(200,299):
        return r.json()['id']

def SpotifySearch(query, s_access_token):
    endpoint="https://api.spotify.com/v1/search"
    
    s_search_headers = {
        "Authorization" : f"Bearer {s_access_token}",
        "Content-Type" : "application/json"
    }

    query_data = urlencode({"q": query, "type": "track", "limit": 1,})
    lookup_url = f"{endpoint}?{query_data}"
    r = requests.get(lookup_url, headers = s_search_headers)
    if r.status_code in range(200,299):
        return r.json()['tracks']['items'][0]['uri']

def SpotifyPlaylistAdd(list_of_uris, s_playlist_id, s_access_token):

    endpoint = f"https://api.spotify.com/v1/playlists/{s_playlist_id}/tracks"
    
    s_playlist_add_headers = {
        "Authorization" : f"Bearer {s_access_token}",
        "Content-Type" : "application/json"
    }
    s_playlist_add_data = {
        "uris" : list_of_uris
    }

    r = requests.post(endpoint, json = s_playlist_add_data, headers = s_playlist_add_headers)
    if r.status_code in range(200,299):
      return 1
    else:
      return 0
    