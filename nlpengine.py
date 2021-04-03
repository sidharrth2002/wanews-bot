from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

stopwords = ENGLISH_STOP_WORDS.union(['Malaysia', 'Malaysian', 'said'])

def subjectivity(text: str):
    return TextBlob(text).sentiment.subjectivity

def polarity(text: str):
    return TextBlob(text).sentiment.polarity

def createCloud(text_list):
    combined = ". ".join(text_list)
    cloud = WordCloud(stopwords=stopwords, width=800, height=400).generate(combined)
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig('./wordclouds/blob.png', facecolor='k', bbox_inches='tight')
    return './wordclouds/blob.png'

if __name__ == '__main__':
    createCloud(['a', 'b', 'c', 'd', 'd'])