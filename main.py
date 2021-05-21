import os
import discord
import re
import json
import asyncio
import requests
from urllib.parse import urlencode

client = discord.Client()


@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #msg = message.content
    if message.content.startswith('$ppls'):
        #main code
        l = 1000
        s_scope = 'playlist-modify-public'
        s_username = 'r4xa4j5m4mjpz14d0kz0v9gfz' #my playlist bot
        s_description = "created by Playlist Bot#7808"
        
        s_client_id = os.environ['SPOTIPY_CLIENT_ID']
        s_client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
        s_access_token = os.environ['SPOTIFY_ACCESS_TOKEN'] #Playlist Bot account

        text_scraper = []
        embedlist = []
        rawlinks = []
        rawnames=[]
        songnames=[]

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
        file2 = open("play_final.txt","w+")

        for i in range(len(embedlist)):
            temp = embedlist[i][0]
            tempdesc = temp.description
            if re.match("^\*", tempdesc):
                #print(tempdesc)
                tempname = re.findall('\[(.*?)\]',tempdesc)
                tempurl = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+',tempdesc)
                #print(tempurl)
                url = tempurl[0]
                #print(url)
                parsed = url.split("=")
                videoId = parsed[1]
                rawlinks.append(videoId)
                rawnames.append(tempname)
        
        pname_embed = discord.Embed(
          title = "What should be the name of your playlist",
          description = "This request will timeout after 1 min"
        )
        pname_embed_sent = await message.channel.send(embed=pname_embed)

        try:
          pname_msg = await client.wait_for('message', timeout=60, check=lambda message: message.author == message.author)
          
          s_playlist_name = pname_msg.content

          if pname_msg:
            await message.channel.send("Your Playlist is being generated")
            #spotifyObject.user_playlist_create(user=s_username,name=s_playlist_name, public=True,description=s_description)
            
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


client.run(os.environ['DISCORD_BOT_TOKEN'])

