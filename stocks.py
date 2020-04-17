import requests
import json
from config import API_KEY, URL

# returns top 5 stock symbols from search keyword
def top5Search(keywords):
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keywords,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    top5 = response.json()['bestMatches'][:5]
    return top5

# return first canadian symbol otherwise return overall top result
def symbolSearch(keywords):
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keywords,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    results = response.json()['bestMatches']
    for stock in results:
        if (stock['4. region'] == 'Toronto'):
            return stock['1. symbol']
            break
    return results[0]['1. symbol']

# return stock data for a given symbol
def stockData(symbol):
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol,
        'apikey': 'SHAJ7XTL7NCWJXNP'
    }
    response = requests.request('GET', URL, params=params)
    results = response.json()
    return results

def currency(number):
    return '$' + "{:.2f}".format(float(number))

# data = stockData(symbolSearch('shopify'))
# print(top5Search('shopify'))
# print(data['Global Quote'])


