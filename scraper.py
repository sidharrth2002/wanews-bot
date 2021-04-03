import os
from sys import executable
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re

def configureSelenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    return driver

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

def getArticleStar(url: str):
    article = requests.get(url);
    soup = BeautifulSoup(article.content, 'html.parser')
    return ' '.join([p.text for p in soup.find(id='story-body').findChildren()])

#page dynamically generated, have to use selenium
def starFootball():
    #if on heroku, configure selenium first
    if(os.environ.get("GOOGLE_CHROME_BIN") and os.environ.get("CHROMEDRIVER_PATH")):
        driver = configureSelenium()
    else:
        driver = webdriver.Chrome()
    URL = 'https://www.thestar.com.my/sport'
    driver.get(URL)
    print(driver.title)

    footballNews = {}

    stories = driver.find_elements_by_xpath("//a[@data-content-category = 'Sport/Football']")
    for story in stories:
        if 'Soccer-' in story.get_attribute('data-content-title'):
            stripped = story.get_attribute('data-content-title').split('Soccer-')[1]
        else:
            stripped = story.get_attribute('data-content-title')

        if stripped not in footballNews.keys():
            footballNews[stripped] = story.get_attribute('href')
    # print(footballNews)
    return footballNews

def malaysiakini():
    URL = 'https://www.malaysiakini.com/'
    classNames = {
        'Top Story': 'jsx-4226912739 title',
        'Top Stories': 'jsx-3163722522',
        'Featured': 'jsx-2425286463 tabPanelTitle'
    }

def mkiniOpinionPieces():
    URL = 'https://www.malaysiakini.com/en/latest/columns'
    classNames = {
        'Title': {
            'tag': 'h3',
            'class': 'jsx-196449950'
        },
        'Summary': {
            'tag': 'div',
            'class': 'jsx-196449950 summary"'
        }
    }