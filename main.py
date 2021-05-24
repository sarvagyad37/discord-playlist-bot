import os
import discord
import re
import asyncio
from keepAlive import KeepAlive
from spotifySelfAPI import SpotifyAuthAccessToken, SpotifySearch, SpotifyPlaylistCreate, SpotifyPlaylistAdd
from replaceBadKeywords import ReplaceBadKeywords
from collections import OrderedDict

client = discord.Client()

@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ppls'):
        #main code
        l = 1000
        uri_limit = 99

        s_client_id = os.environ['SPOTIFY_CLIENT_ID']
        s_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
        s_refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']

        text_scraper = []
        embedlist = []
        rawnames = []
        songnames = []
        s_rawuri=[]
        s_temprawuri = []

        async for msg in message.channel.history(limit=l):
            text_scraper.append([msg.content, msg.created_at, msg.author.name])

        for i in range(l):
            if (re.match(r"^:thumbsup:", text_scraper[i][0])) and (text_scraper[i][2] == "Rythm"):
                n = i
                break

        t1 = text_scraper[n][1]
        print(t1)
        async for msg in message.channel.history(limit=l, after=t1):
            if msg.embeds:  #MIND BLOWING TECHNIQUE TO CHECK EMPTY LIST
                embedlist.append(msg.embeds)

        file1 = open("playlist.txt", "w+")
        s_access_token = SpotifyAuthAccessToken(s_client_id, s_client_secret, s_refresh_token)

        for i in range(len(embedlist)):
            temp = embedlist[i][0]
            tempdesc = temp.description
            if re.match("^\*", tempdesc):
                tempname = re.findall('\[(.*?)\]', tempdesc) #list of one item
                tempname = ReplaceBadKeywords(tempname[0])
                try:
                    s_tempuri = SpotifySearch(tempname, s_access_token)
                    s_temprawuri.append(s_tempuri)
                except IndexError:
                    #add to file all songs which doesnt get searched
                    pass
                rawnames.append(tempname)

        pname_embed = discord.Embed(
            title="What should be the name of your playlist",
            description="This request will timeout after 1 min"
            )
        pname_embed_sent = await message.channel.send(embed=pname_embed)

        try:
            def check(m):
                return m.author == message.author and m.channel == message.channel

            pname_msg = await client.wait_for(
                'message',
                timeout=60,
                check=check)

            s_playlist_name = pname_msg.content

            if pname_msg:
                await message.channel.send("Your Playlist is being generated")
                
                s_playlist_id = SpotifyPlaylistCreate(s_playlist_name, s_access_token)
                s_rawuri = list(OrderedDict.fromkeys(s_temprawuri))

                s_uri = [s_rawuri[i:i + uri_limit] for i in range(0, len(s_rawuri), uri_limit)]

                for j in range(len(s_uri)):
                    SpotifyPlaylistAdd(s_uri[j], s_playlist_id, s_access_token)
                s_playlist_link = f"http://open.spotify.com/user/r4xa4j5m4mjpz14d0kz0v9gfz/playlist/{s_playlist_id}"

                await message.channel.send(s_playlist_link)

        except asyncio.TimeoutError:
            await pname_embed_sent.delete()
            await message.channel.send("Cancelling due to timeout", delete_after=10)

        songnames = list(map(''.join, rawnames))
        for i in range(len(songnames)):
            file1.write(songnames[i])
            file1.write('\n')

        file1.close()

        print("hogya")

KeepAlive()
client.run(os.environ['DISCORD_BOT_TOKEN'])
