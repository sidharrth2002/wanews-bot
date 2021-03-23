import requests
from bs4 import BeautifulSoup

def scrapeStar():
    staronlineURL = 'https://www.thestar.com.my/'
    staronline = requests.get(staronlineURL)

    soup = BeautifulSoup(staronline.content, 'html.parser')

    stories = {}

    featured_stories_nation = {}
    for story in soup.find_all('a', { "data-list-type": "Featured Stories", "data-content-category": "News/Nation" }):
        featured_stories_nation[story["data-content-title"]] = story['href']
    stories['Featured Stories Nation'] = featured_stories_nation

    featured_stories_asean = {}
    for story in soup.find_all('a', { "data-list-type": "Featured Stories", "data-content-category": "AseanPlus/Aseanplus News"}):
        featured_stories_asean[story["data-content-title"]] = story['href']
    stories['Featured Stories Asean'] = featured_stories_asean

    return stories