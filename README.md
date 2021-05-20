# Wanews

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Natural Language Processing Powered bot that curates news stories from various news sources, performs sentiment analysis and NER before delivering output through a Discord interface. 🚀

This bot is not only an incredibly powerful realtime scraper, it also incorporates a Natural Language Processing Engine powered by Spacy, NLTK and Gensim that effectively summarise the news of the day. 

The bot currently retrieves information from the following sources:
1. The Star
2. Malay Mail
3. Malaysiakini- To be released soon
4. The New York Times API
5. Rapid News API for International Headlines

### Word Clouds with the day's key players

<img src='https://user-images.githubusercontent.com/53941721/118935907-9ca4dc80-b97e-11eb-819c-ba34b22d4bf3.png' width='500'>

### Curated National Headlines

<img width="544" alt="Screenshot 2021-05-20 at 3 20 57 PM" src="https://user-images.githubusercontent.com/53941721/118936808-73d11700-b97f-11eb-8d58-7616f08a85f4.png">

### Football Headlines

<img width="417" alt="Screenshot 2021-05-20 at 3 26 05 PM" src="https://user-images.githubusercontent.com/53941721/118937165-cdd1dc80-b97f-11eb-88ea-7d2848104684.png">

### Functionality that is available but not deployed:
1. Redis caching- Instead of scraping upon a call to the bot, scrape periodically and cache news stories. 

### How to use this bot?
If you are running your local Python interpretation through virtual environments, create a new one (I use virtualenvwrapper). Clone this repository and create a `.env` file that contains the following:

```
DISCORD_TOKEN = 
DISCORD_GUILD = 
NEWS_API_KEY = 
NYTIMES_API_KEY = 
VERSION = DEVELOPMENT or PRODUCTION
```

and run:
```
pip3 install requirements.txt
```
then
```
python bot.py
```

If you're interested in extending the news organisations this scrapes from, feel free to submit pull requests. Cheers!
