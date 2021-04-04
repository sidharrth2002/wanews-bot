from collections import defaultdict
from numpy import pad
from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import uuid

stopwords = ENGLISH_STOP_WORDS.union(['Malaysia', 'Malaysian', 'said', 'Datuk', 'Seri'])

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

def ner(text_list):
    allsentences = ' '.join(text_list)
    sentences_tokenized = sent_tokenize(allsentences)
    token_sentences = [word_tokenize(sent) for sent in sentences_tokenized]
    pos_sentences = [nltk.pos_tag(sent) for sent in token_sentences]

    chunked_sentences_binary = nltk.ne_chunk_sents(pos_sentences, binary=True)
    named_entities = []
    
    for sent in chunked_sentences_binary:
        for chunk in sent:
            if hasattr(chunk, 'label') and chunk.label() == 'NE':
                named_entities.append(' '.join(c[0] for c in chunk))

    main_entities = WordCloud(stopwords=stopwords, background_color="black", width=800, height=400).generate(' '.join(list(dict.fromkeys(named_entities))))
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