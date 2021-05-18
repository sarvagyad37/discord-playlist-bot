import os
import discord
import re
from ytmusicapi import YTMusic
#YTMusic.setup(filepath=headers_auth.json)
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
        l=1000
        text_scraper = []
        embedlist=[]
        rawlinks=[]
        #urls=[]
        async for msg in message.channel.history(limit=l):
            if (msg.author.name)=="Rythm":
              text_scraper.append([msg.content, msg.created_at])  
        #print(text_scraper)
        #print(" ")

        for i in range(l):
          if re.match(r"^:thumbsup:",text_scraper[i][0]):
            n=i
            break
        #print(n)
        #print(text_scraper[n][1])
        t1=text_scraper[n][1]
        print(t1)
        #session1_text_scraper = text_scraper[:n]
        async for msg in message.channel.history(limit=l, after=t1):
          if msg.embeds: #MIND BLOWING TECHNIQUE TO CHECK EMPTY LIST
            embedlist.append(msg.embeds)
        #print(embedlist)
        file1 = open("playlist.txt","w+")
        #file2 = open("play_final.txt","w+")
        for i in range(len(embedlist)):
          temp=embedlist[i][0]
          tempdesc=temp.description
          if re.match("^\*", tempdesc):
            tempurl = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', tempdesc)
            url_ID = re.sub("/(https?)?+(:\/\/?)?+(www.?)?+[a-zA-Z]+(.com|.be)+(\/)+(watch?)?+[(?)]?+(v=?|V=?)?|(&)+(.*)/", "",tempurl)
            print(url_ID)
            rawlinks.append(url_ID)
        #print(rawlinks)
        urls = list(map(''.join, rawlinks))
        for i in range(len(urls)):
          file1.write(urls[i])
          file1.write('\n')
        #file1.writelines(urls)
        #raw_urls=[]
        file1.close()
        file1 = open("playlist.txt","r")
        f = discord.File(file1)
        await message.channel.send(file=f)
        file1.close()
        print("hogya")

    if message.content.startswith('$pppls'):
      l=11
      embedlist=[]
      async for msg in message.channel.history(limit=l):
        if msg.embeds: #MIND BLOWING TECHNIQUE TO CHECK EMPTY LIST
          embedlist.append(msg.embeds)
      #print(embedlist)
      for i in range(len(embedlist)):
        temp=embedlist[i][0]
        print(temp.title, temp.description)
        


    if message.content.startswith('$embed'):
        embeds = message.embeds
        for embed in embeds:
          print(embed.to_dict())
    if message.content.startswith('thank you supriya'):
        await message.channel.send("SUPRIYA IS THE BESTTTT!!!!")
    if message.content.startswith('$plshelpmedha'):
        await message.channel.send("FUCK OFF MEDHA LEMME DO MY JOB")
    elif message.content.startswith('$plshelp'):
        await message.channel.send("sorry babe, i am still a work in progress")
    elif message.content.startswith('$plshelp '):
        await message.channel.send("sorry babe, i am still a work in progress")



client.run(os.environ['TOKEN'])
