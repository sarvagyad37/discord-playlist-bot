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
            text_scraper.append([msg.content, msg.created_at, msg.author.name])  #max(datetime.datetime) for newest
            #if msg.content.lower() == match_re:
        print(text_scraper)
        print(" ")
        text_scraper_rev=text_scraper[::-1]
        print(text_scraper_rev)

        for i in range(l):
          #if text_scraper[i][0] == re.match(r"^:thumbsup: **Joined",text_scraper[i][0])



client.run(os.environ['TOKEN'])
