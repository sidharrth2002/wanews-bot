'''
NLP Utilities
'''

from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import spacy
import uuid

nlp = spacy.load('en_core_web_sm')

stopwords = ENGLISH_STOP_WORDS.union(['Malaysia', 'Malaysian', 'said', 'Datuk', 'Seri'])

def subjectivity(text: str):
    return TextBlob(text).sentiment.subjectivity

def polarity(text: str):
    return TextBlob(text).sentiment.polarity

def classify(sentiment: dict):
    if(sentiment['polarity'] < 0):
        return '😟'
    elif (sentiment['polarity'] == 0):
        return '😐'
    else:
        return '😊'

def createCloud(text_list):
    combined = ". ".join(text_list)
    cloud = WordCloud(stopwords=stopwords, width=800, height=400).generate(combined)
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig('./wordclouds/blob.png', facecolor='k', bbox_inches='tight')
    return './wordclouds/blob.png'

def ner(text_list):
    doc = nlp(' '.join(text_list))
    entities = [ent.text.replace(" ", "") if len(ent.text.split()) != 0 else ent.text for ent in list(doc.ents)] 
    main_entities = WordCloud(stopwords=stopwords, background_color="black", width=800, height=400).generate(' '.join(list(entities)))
    plt.figure(figsize=(20,20))
    plt.imshow(main_entities, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    #use uuid to track images, so overwriting doesn't become a problem
    location = './wordclouds/' + str(uuid.uuid1()) + '.png'
    plt.savefig(location, facecolor='k', bbox_inches='tight')
    return location

if __name__ == '__main__':
    createCloud(['a', 'b', 'c', 'd', 'd'])