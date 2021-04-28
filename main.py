import discord
import os
from riotwatcher import LolWatcher, ApiError
import pandas as pd
from dotenv import load_dotenv, find_dotenv

#Testing
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
        username = message.content[5:]
        username = username.replace(' ', '')
        link = "https://na.op.gg/summoner/userName="+ username 
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
        matches = watcher.champion_mastery.by_summoner(my_region, me['id'])
        print(matches)
        teststats= watcher.champion.rotations(my_region)
        #print(teststats)
        
        embed = discord.Embed(
        title = my_ranked_stats[0]['summonerName'],
        description = my_ranked_stats[0]['tier'],
        colour = discord.Colour.blue()
        )

        embed.set_thumbnail(url='https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltdd9ba3a2e063f047/5fdc3abd02fd0c7d345f132a/Compet.png')
        embed.add_field(name='Wins', value=my_ranked_stats[0]['wins'], inline=True)
        embed.add_field(name='Losses', value=my_ranked_stats[0]['losses'], inline=True)
        embed.add_field(name='Win %', value=round((my_ranked_stats[0]['wins']/(my_ranked_stats[0]['losses']+ my_ranked_stats[0]['wins']))*100,2), inline=True)
        embed.add_field(name='More Stats', value=(link), inline=False)
        
        await message.channel.send(embed=embed)



    
client.run(os.getenv('API_KEY'))
