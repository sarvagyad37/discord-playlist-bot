import os
import discord
import re

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
    
        #match_re =
        l=11
        text_scraper = []
        async for msg in message.channel.history(limit=l):
            text_scraper.append([msg.content, msg.author.name])  #max(datetime.datetime) for newest
        #print(text_scraper)
        #print(" ")

        for i in range(l):
          if re.match(r"^:thumbsup:",text_scraper[i][0]):
            n=i
            break
        #print(n)
        #print(text_scraper[n][1])
        #t1=text_scraper[n][1]
        session1_text_scraper = text_scraper[:n]




client.run(os.environ['TOKEN'])
