import requests
import json
from config import API_KEY, URL

# returns top 5 stock results from search result
def top5Search(keyword):
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keyword,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    top5 = response.json()['bestMatches'][:5]
    return top5

# return top search result (prioritizing TSX stocks)
def symbolSearch(keyword):
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keyword,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    results = response.json()['bestMatches']
    for stock in results:
        if (stock['4. region'] == 'Toronto'):
            return stock
            break
    return results[0]

# return stock data for a given symbol
def getStockData(symbol):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    results = response.json()
    return results['Global Quote']

# format number to currency 
def currencyFormat(number):
    return '$' + "{:.2f}".format(float(number))



