from ytmusicapi import YTMusic
ytmusic = YTMusic('headers_auth.json')
import youtube_dl

id1 = ['vU05Eksc_iM','gJgHSLAxXYc']
#playlistId = ytmusic.create_playlist(title = "test",description = "desc", video_ids = id1, privacy_status="UNLISTED")
#print(playlistId)
search_results = ytmusic.search("TAYLORSWIFT - Evermore (Music Video Official Lyrics)", "songs", limit= 0)
song_title = search_results[0]['title']
artist_name = search_results[0]['artists'][0]['name']
final_res = f"{song_title} {artist_name}"
print(final_res)
#ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

#TAYLORSWIFT - Evermore Full Album (Deluxe Edition)
