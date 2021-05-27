import os
import discord
import re
import asyncio
from keepAlive import KeepAlive
from spotifySelfAPI import SpotifyAuthAccessToken, SpotifySearch, SpotifyPlaylistCreate, SpotifyPlaylistAdd
from replaceBadKeywords import ReplaceBadKeywords
from collections import OrderedDict
from youtubeSelfAPI import YoutubePlaylistCreate, YoutubeSearch, YoutubePlaylistAdd
import time

client = discord.Client()

@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ppls'):
        start = time.time()
        print("chaliye shuru karte hai")
        #main code
        l = 10000
        req_limit = 50

        s_client_id = os.environ['SPOTIFY_CLIENT_ID']
        s_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        s_refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']

        text_scraper = []
        embedlist = []
        rawnames = []
        songnames = []
        s_rawuri=[]
        s_temprawuri = []
        name_id_pair = []
        tempembedlist = []

        async for msg in message.channel.history(limit=l):
          if (msg.author.name == "Rythm"):
            text_scraper.append([msg.content])
            embedlist.append(msg.embeds)
            if (re.match(r"^:thumbsup:", msg.content)):
              break

        

        try:
            #for i in range(len(text_scraper)):
             #   if (re.match(r"^:thumbsup:", text_scraper[i][0])):
               #     n = i
               #     break
            n = len(text_scraper)
            #t1 = text_scraper[n][1]
            #new_text_scraper = text_scraper[:n+1]
            new_embedlist = embedlist[:n+1]

        except UnboundLocalError:
            raise Exception("init message before l=1000")
            #l=l+250

        for i in range(n):
            if new_embedlist[i]: #MIND BLOWING TECHNIQUE TO CHECK EMPTY LIST
              tempembedlist.append(new_embedlist[i])

        file1 = open("playlist.txt", "w+")
        s_access_token = SpotifyAuthAccessToken(s_client_id, s_client_secret, s_refresh_token)

        pplatform_embed = discord.Embed(
            title="Do you want playlist on Spotify or Youtube Music?\nType y for youtube music or type s for spotify",
            description="This request will timeout after 1 min"
            )
        pplatform_embed_sent = await message.channel.send(embed=pplatform_embed)

        try:
            def check(m):
                return m.author == message.author and m.channel == message.channel

            pplatform_msg = await client.wait_for(
                'message',
                timeout=60,
                check=check)

            platform_name = pplatform_msg.content

            for i in range(len(tempembedlist)):
                temp = tempembedlist[i][0]
                tempdesc = temp.description
                if re.match("^\*", tempdesc):
                    tempurl = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+',tempdesc)

                    try:
                        url = tempurl[0]
                        parsed = url.split("=")
                        y_videoId = parsed[1]
                    except:
                        y_videoId = None
                        print("printing none videoID")
                        pass

                    tempname = re.findall('\[(.*?)\]', tempdesc) #list of one item
                    try:
                      tempname = ReplaceBadKeywords(tempname[0])
                    except:
                      pass
                    tempkv = [tempname, y_videoId]
                    name_id_pair.append(tempkv)
            #print(len(name_id_pair))

            if pplatform_msg:
              pname_embed = discord.Embed(
                  title="What should be the name of your playlist",
                  description="This request will timeout after 1 min"
                  )
              pname_embed_sent = await message.channel.send(embed=pname_embed)

              try:
                  pname_msg = await client.wait_for(
                      'message',
                      timeout=60,
                      check=check)

                  playlist_name = pname_msg.content

                  if pname_msg:  
                      if (platform_name == "y") or (platform_name == "youtube") :
                          y_playlist_id = YoutubePlaylistCreate(playlist_name)
                          y_rawvideoIds = [k[1] for k in name_id_pair]
                          #print(len(y_rawvideoIds))
                          y_videoIds = [y_rawvideoIds[i:i + req_limit] for i in range(0, len(y_rawvideoIds), req_limit)]
                          #print(len(y_videoIds))

                          await message.channel.send("Your Youtube Playlist is being generated")

                          #k = YoutubePlaylistAdd(y_rawvideoIds, y_playlist_id)

                          #print(k)

                          for j in range(len(y_videoIds)):
                              YoutubePlaylistAdd(y_videoIds[j], y_playlist_id)
                          #    sleep(5)
                          #    print(k)
                              
                          y_playlist_link = f"https://music.youtube.com/playlist?list={y_playlist_id}"

                          await message.channel.send(y_playlist_link)            

                      if (platform_name == "s") or (platform_name == "spotify") :
                          for i in range(len(name_id_pair)):
                              try:
                                  s_tempuri = SpotifySearch(name_id_pair[i][0], s_access_token)
                                  s_temprawuri.append(s_tempuri)
                              except IndexError:
                                  try:
                                      song_name = YoutubeSearch(name_id_pair[i][0])
                                      s_tempuri = SpotifySearch(song_name, s_access_token)
                                      s_temprawuri.append(s_tempuri)
                                  except IndexError:
                                      print("idk somethings wrong but ok, video list:", name_id_pair[i])
                                  
                          
                          await message.channel.send("Your Spotify Playlist is being generated")

                          s_playlist_id = SpotifyPlaylistCreate(playlist_name, s_access_token)
                          
                          s_rawuri = list(OrderedDict.fromkeys(s_temprawuri))

                          s_uri = [s_rawuri[i:i + req_limit] for i in range(0, len(s_rawuri), req_limit)]

                          for j in range(len(s_uri)):
                              SpotifyPlaylistAdd(s_uri[j], s_playlist_id, s_access_token)
                          s_playlist_link = f"http://open.spotify.com/user/r4xa4j5m4mjpz14d0kz0v9gfz/playlist/{s_playlist_id}"

                          await message.channel.send(s_playlist_link)
                      #else:
                        #await message.channel.send("you didnt enter a valid response, kindly run the bot again")

              except asyncio.TimeoutError:
                  await pname_embed_sent.delete()
                  await message.channel.send("Cancelling due to timeout", delete_after=10)

        except asyncio.TimeoutError:
            await pplatform_embed_sent.delete()
            await message.channel.send("Cancelling due to timeout", delete_after=10)

        songnames = list(map(''.join, rawnames))
        for i in range(len(songnames)):
            file1.write(songnames[i])
            file1.write('\n')

        file1.close()

        print("hogya")
        end = time.time()
        print(f"Runtime of the program is {end - start}")


KeepAlive()
client.run(os.environ['DISCORD_BOT_TOKEN'])
