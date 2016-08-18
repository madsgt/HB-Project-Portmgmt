from sys import argv #argv is a list containing the arguments passed to the python interpreter when called from a command line
import pprint #pretty print
# from simplejson import json #API might return json string
import requests # to get the url
import datetime #get the timestamp right
import os # to access the os environment variables
import urllib2
import yahoo_finance
from werkzeug.contrib.cache import FileSystemCache
import optimization
# from pandas.io.data import DataReader #to work with such time series in Python

# make a printer
printer = pprint.PrettyPrinter()





def get_single_stock_data(ticker):

    """get single stock data that takes in a single ticker symbol and returns a dictionary

        Expected data
            [{'Adj_Close': '28.35',
            'Close': '28.35',
            'Date': '2013-08-12',
            'High': '28.370001',
            'Low': '27.50',
            'Open': '27.549999',
            'Symbol': 'YHOO',
            'Volume': '16561900'}] """



    symbol = yahoo_finance.Share(ticker)
    past_date = datetime.datetime.now() - datetime.timedelta(days=3*365)
    str_past_date = datetime.datetime.strftime(past_date, "%Y-%m-%d")
    str_today_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    ticker_data = symbol.get_historical(str_past_date, str_today_date)

    data_needed = [result['Adj_Close'] for result in ticker_data if 'Adj_Close' in result]
    print {ticker: data_needed}




def get_all_stock_data(tickers):
    """ takes in a list of ticker symbols and returns a dictionary of data"""

    
    historicaldata = []

    for ticker in tickers:

        onequote = get_single_stock_data(ticker)
        historicaldata.append(onequote)

    historicalreturns = optimization.historical_returns(historicaldata)    
    portfolio = optimization.optimal_portfolio(historicalreturns) 
      
    return portfolio





if __name__=="__main__":

    test = get_all_stock_data(["GOOG","YHOO"]) 
    # need to pull data for 2 to 5 stocks and store this ,make this dynamic
    printer.pprint(test)
