import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get
import requests
from scraper import scrapeStar, starFootball, getArticleStar
from nlpengine import createCloud
import datetime
import redis
r = redis.Redis()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NYTIMES_API_KEY = os.getenv('NYTIMES_API_KEY')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print('News Bot fired up')

@bot.command(name='sports')
async def sportsHeadlines(ctx):
    await ctx.channel.send('Here are Curated Sports Headlines (Beware of Tabloids)')
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=gb&category=sports&apiKey={NEWS_API_KEY}')
    if(response.status_code == 200):
        response = response.json()
        print(response)
        embed=discord.Embed(title="Sports Headlines", description="Curated From Sources Around the World", color=0xff0000)
        for i, article in enumerate(response['articles']):
            embed.add_field(name=str(i+1) + ") ", value= article['title'] + f" [Read More]({article['url']})", inline=False)

        embed.set_footer(text="Powered by NewsAPI")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send('Cannot Currently Connect to the API.')

@bot.command(name='thestar')
async def staronline(ctx):
    stories = scrapeStar()
    nation_featured = stories['Featured Stories Nation']
    asean = stories['Featured Stories Asean']

    embed=discord.Embed(title="National Headlines", description="Scraped from the Star Online", color=0xff0000)
    
    for i, story in enumerate(list(nation_featured.keys())):
        embed.add_field(name=str(i+1) + ") ", value=story + f" [Read More]({nation_featured[story]})", inline=False)
    
    await ctx.channel.send(embed=embed)

@bot.command(name='nytimes')
async def nytimes(ctx):
    await ctx.channel.send('NY Times')
    response = requests.get(f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key={NYTIMES_API_KEY}')
    if(response.status_code == 200):
        articles = response.json()['results']
        embed=discord.Embed(title="NYTimes Top Stories", description="A Collection of The Most Popular Articles on the New York Times", color=0xff0000)
        for i, article in enumerate(articles):
            embed.add_field(name=article['title'], value=article['abstract'] + f" [Read More]({article['url']})" + "\n", inline=False)
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send('Having trouble connecting to the NYTimes API')

@bot.command(name='football')
async def footballNews(ctx):
    await ctx.channel.send('Scraping Realtime Football News. Give me a second.')
    stories = starFootball()
    embed=discord.Embed(title="Football News", description="Football News Scraped From the Star", color=0xff0000)
    for story in stories.keys():
        embed.add_field(name=story, value= f" [Read More]({stories[story]})", inline=False)
    
    await ctx.channel.send(embed=embed)

@bot.command(name='help')
async def help(ctx):
    embed=discord.Embed(title="Commands Available", description="Here are commands you can try.", color=0xff0000)
    embed.add_field(name="!sports", value="Sports Headlines From Around the World", inline=False)
    embed.add_field(name="!thestar", value="National headlines from the star", inline=False)
    embed.add_field(name='!nytimes', value="Most Read Stories in the New York Times", inline=False)
    embed.add_field(name='!football', value="Football news from the star", inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(name='overview')
async def overview(ctx):
    await ctx.channel.send('''Here are major words that appeared in news articles this week.
                            This might take a while as the NLP engine is scraping and processing news articles.
                            ''')
    articles = scrapeStar()
    urls = []
    for category in articles:
        urls += list(articles[category].values())
    print(urls)
    articleData = [getArticleStar(url) for url in urls]
    print(articleData)
    cloudLocation = createCloud(articleData)
    with open(cloudLocation, 'rb') as f:
        picture = discord.File(f)
        await ctx.channel.send(file=picture)

@bot.command(name='bigplayers')
async def bigplayers(ctx):
    print('Who did the news talk about?')

#scrape every half an hour and store in redis to speed up NLP stuff
@tasks.loop(minutes=30.0)
def task():
    print('Fetching Everything')
    stararticles = scrapeStar()
    football = starFootball()
    urls = []
    for category in stararticles:
        urls += list(stararticles[category].values())
    articleBodies = {}
    for url in urls:
        articleBodies[url] = getArticleStar(url)
    print(stararticles)
    print(football)

    r.hset("Star- Featured Stories Nation", None, None, stararticles['Featured Stories Nation'])
    if(len(stararticles['Featured Stories Asean']) != 0):
        r.hset("Star- Featured Stories Asean", None, None, stararticles['Featured Stories Asean'])
    r.hset('Football', None, None, football)
    r.hset('Article Bodies', None, None, articleBodies)

    print(r.hgetall("Article Bodies"))

task()
bot.run(TOKEN)