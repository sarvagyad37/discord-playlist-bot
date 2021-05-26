from ytmusicapi import YTMusic

def YoutubePlaylistCreate(playlist_name):
    ytmusic = YTMusic('headers_auth.json')
    playlist_id = ytmusic.create_playlist(title = playlist_name, description = "TPWK :)", privacy_status = 'UNLISTED')
    return playlist_id

def YoutubeSearch(query):
    ytmusic = YTMusic('headers_auth.json')
    search_results = ytmusic.search(query, "songs")
    song_title = search_results[0]['title']
    artist_name = search_results[0]['artists'][0]['name']
    final_res = f"{song_title} {artist_name}"
    return final_res
    
def YoutubePlaylistAdd(list_of_videoIds, playlist_id):
    ytmusic = YTMusic('headers_auth.json')
    ytmusic.add_playlist_items(playlist_id, list_of_videoIds)
