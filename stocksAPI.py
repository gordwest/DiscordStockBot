import requests
import json
from config import API_KEY, URL

# not used
def top5Search(keyword):
    """ Search for a keyword and return the top 5 stock results
    """
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keyword,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    top5 = response.json()['bestMatches'][:5]
    return top5


def stockSearch(keyword):
    """ Search for a stock given a keyword and return the top search result (prioritizing TSX stocks)
    params
        keyword: string - what the user is trying to search
    returns
        JSON data for the stock from the searcdh results
    """
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
def getStockData(stockSymbol):
    """ Search for a stock given its symbol and return a dictionary of information for the result
    params
        stockSymbol: string - the symbol of a specific stock
    returns
        JSON data for the given stock
    """
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': stockSymbol,
        'apikey': API_KEY
    }
    response = requests.request('GET', URL, params=params)
    results = response.json()
    return results['Global Quote']

# format number to currency 
def currencyFormat(number):
    """
    """
    return '$' + "{:.2f}".format(float(number))
