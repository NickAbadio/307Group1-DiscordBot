import discord
import os
from riotwatcher import LolWatcher, ApiError
import pandas as pd
from dotenv import load_dotenv, find_dotenv

#Git hub Testing
load_dotenv(find_dotenv())

client = discord.Client()
api_key = os.getenv('RIOT_TOKEN')
watcher = LolWatcher(api_key)
my_region = 'na1'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$User'):
        me = watcher.summoner.by_name(my_region, message.content[5:])
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
        
        embed = discord.Embed(
        title = my_ranked_stats[0]['summonerName'],
        description = my_ranked_stats[0]['tier'],
        colour = discord.Colour.blue()
        )
        embed.set_thumbnail(url='https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltdd9ba3a2e063f047/5fdc3abd02fd0c7d345f132a/Compet.png')
        embed.add_field(name='Wins', value=my_ranked_stats[0]['wins'], inline=False)
        embed.add_field(name='Losses', value=my_ranked_stats[0]['losses'], inline=False)
        
        await message.channel.send(embed=embed)



    
client.run(os.getenv('API_KEY'))
