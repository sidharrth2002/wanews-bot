'''
Other Uitilities
'''

import requests

def getQuote():
    response = requests.get('https://zenquotes.io/api/random')
    return (response.json()[0]['q'] + '  - ' + response.json()[0]['a'])

if __name__ == '__main__':
    getQuote()