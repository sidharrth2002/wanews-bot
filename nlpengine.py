from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

stopwords = ENGLISH_STOP_WORDS

def subjectivity(text: str):
    return TextBlob(text).sentiment.subjectivity

def polarity(text: str):
    return TextBlob(text).sentiment.polarity

def createCloud(text_list):
    combined = ". ".join(text_list)
    cloud = WordCloud(stopwords=ENGLISH_STOP_WORDS, width=500, height=300).generate(combined)
    plt.figure(figsize=(15,15))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('./wordclouds/blob.png')

if __name__ == '__main__':
    createCloud(['a', 'b', 'c', 'd', 'd'])