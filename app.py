import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
import requests

from scraper import scrapeStar

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('News Bot fired up')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(guild)
    print(f'The current guild is {guild.name}')

    memberlist = [member.name for member in guild.members]
    print(memberlist)

@bot.command(name='sportsHeadlines')
async def sportsHeadlines(ctx):
    await ctx.channel.send('Here are Curated Sports Headlines (Beware of Tabloids)')
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=my&category=sports&apiKey={NEWS_API_KEY}').json()
    print(response)

    embed=discord.Embed(title="Sports Headlines", description="Curated From Sources Around the World", color=0xff0000)
    for i, article in enumerate(response['articles']):
        embed.add_field(name=str(i+1) + ") ", value= article['title'] + f" [Read More]({article['url']})", inline=False)

    embed.set_footer(text="Powered by NewsAPI")
    await ctx.send(embed=embed)

@bot.command(name='thestar')
async def startonline(ctx):
    stories = scrapeStar()
    nation_featured = stories['Featured Stories Nation']
    asean = stories['Featured Stories Asean']

    embed=discord.Embed(title="National Headlines", description="Scraped from the Star Online", color=0xff0000)
    
    for i, story in enumerate(list(nation_featured.keys())):
        embed.add_field(name=str(i+1) + ") ", value=story + f" [Read More]({nation_featured[story]})", inline=False)
    
    await ctx.send(embed=embed)


bot.run(TOKEN)