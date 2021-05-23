import os
import discord
import re
import asyncio
import requests
from urllib.parse import urlencode
import base64
from keep_alive import keep_alive

client = discord.Client()


@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    def SpotifyAuthAccessToken():
      
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

    def SpotifyPlaylistCreate(s_playlist_name):
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

    def SpotifySearch(query):
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

    def SpotifyPlaylistAdd(list_of_uris):

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


    #msg = message.content
    if message.content.startswith('$ppls'):
        #main code
        l = 1000
        uri_limit = 99

        s_client_id = os.environ['SPOTIFY_CLIENT_ID']
        s_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        s_refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']

        text_scraper = []
        embedlist = []
        rawlinks = []
        rawnames = []
        songnames = []
        s_rawuri=[]

        async for msg in message.channel.history(limit=l):
            text_scraper.append([msg.content, msg.created_at, msg.author.name])
        #print(text_scraper)
        #print(" ")

        for i in range(l):
            if (re.match(r"^:thumbsup:", text_scraper[i][0])) and (text_scraper[i][2] == "Rythm"):
                n = i
                break

        #print(n)
        t1 = text_scraper[n][1]
        print(t1)
        async for msg in message.channel.history(limit=l, after=t1):
            if msg.embeds:  #MIND BLOWING TECHNIQUE TO CHECK EMPTY LIST
                embedlist.append(msg.embeds)
        #print(embedlist)

        file1 = open("playlist.txt", "w+")
        file2 = open("play_final.txt", "w+")
        s_access_token = SpotifyAuthAccessToken()

        for i in range(len(embedlist)):
            temp = embedlist[i][0]
            tempdesc = temp.description
            if re.match("^\*", tempdesc):
                #print(tempdesc)
                tempname = re.findall('\[(.*?)\]', tempdesc) #list of one item
                tempname = re.sub(r'\([^()]*\)', '', tempname[0])
                tempname = re.sub(r'\[[^()]*\]', '', tempname)
                tempname = re.sub(r'\[[^()]*', '', tempname)
                tempurl = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', tempdesc)
                try:
                    s_tempuri = SpotifySearch(tempname)
                    s_rawuri.append(s_tempuri)
                except IndexError:
                    pass
                #word "lyrics" is BAD, doesnt show any search result in spotify with that word
                #print(tempurl)
                
                url = tempurl[0]
                #print(url)
                parsed = url.split("=")
                try:
                  videoId = parsed[1]
                except IndexError:
                  pass
                rawlinks.append(videoId)
                rawnames.append(tempname)

        pname_embed = discord.Embed(
            title="What should be the name of your playlist",
            description="This request will timeout after 1 min"
            )
        pname_embed_sent = await message.channel.send(embed=pname_embed)

        try:
            pname_msg = await client.wait_for(
                'message',
                timeout=60,
                check=lambda message: message.author == message.author)

            s_playlist_name = pname_msg.content

            if pname_msg:
                await message.channel.send("Your Playlist is being generated")
                
                s_playlist_id = SpotifyPlaylistCreate(s_playlist_name)
                s_uri = [s_rawuri[i:i + uri_limit] for i in range(0, len(s_rawuri), uri_limit)]
                for j in range(len(s_uri)):
                    SpotifyPlaylistAdd(s_uri[j])
                s_playlist_link = f"http://open.spotify.com/user/r4xa4j5m4mjpz14d0kz0v9gfz/playlist/{s_playlist_id}"

                await message.channel.send(s_playlist_link)

        except asyncio.TimeoutError:
            await pname_embed_sent.delete()
            await message.channel.send("Cancelling due to timeout", delete_after=10)

        songnames = list(map(''.join, rawnames))
        for i in range(len(songnames)):
            file1.write(songnames[i])
            file1.write('\n')

        urls = list(map(''.join, rawlinks))
        for i in range(len(urls)):
            file2.write(urls[i])
            file2.write('\n')

        file1.close()
        file2.close()
        file1 = open("playlist.txt", "r")
        f1 = discord.File(file1)
        #await message.channel.send(file=f1)
        file1.close()

        file2 = open("play_final.txt", "r")
        f2 = discord.File(file2)
        #await message.channel.send(file=f2)
        file2.close()

        print("hogya")

    if message.content.startswith('thank you supriya'):
        await message.channel.send("SUPRIYA IS THE BESTTTT!!!!")
    if message.content.startswith('$plshelpmedha'):
        await message.channel.send("FUCK OFF MEDHA LEMME DO MY JOB")
    elif message.content.startswith('$plshelp'):
        await message.channel.send("sorry babe, i am still a work in progress")
    elif message.content.startswith('$plshelp '):
        await message.channel.send("sorry babe, i am still a work in progress")

keep_alive()
client.run(os.environ['DISCORD_BOT_TOKEN'])
