import os
import discord
import re
from ytmusicapi import YTMusic

ytmusic = YTMusic('headers_auth.json')

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
        text_scraper = []
        embedlist = []
        rawlinks = []
        rawnames=[]
        songnames=[]
        async for msg in message.channel.history(limit=l):
            if (msg.author.name) == "Rythm":
                text_scraper.append([msg.content, msg.created_at])
        #print(text_scraper)
        #print(" ")

        for i in range(l):
            if re.match(r"^:thumbsup:", text_scraper[i][0]):
                n = i
                break
        #print(n)
        #print(text_scraper[n][1])
        t1 = text_scraper[n][1]
        print(t1)
        #session1_text_scraper = text_scraper[:n]
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
                print(tempurl)
                #print(type(tempurl))
                url = tempurl[0]
                print(url)
                parsed = url.split("=")
                videoId = parsed[1]
                rawlinks.append(videoId)
                rawnames.append(tempname)
        
        #print(rawlinks)
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
        await message.channel.send(file=f1)
        file1.close()

        file2 = open("play_final.txt", "r")
        f2 = discord.File(file2)
        await message.channel.send(file=f2)
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


client.run(os.environ['TOKEN'])
