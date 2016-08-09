from sys import argv #argv is a list containing the arguments passed to the python interpreter when called from a command line
import pprint #pretty print
# from simplejson import json #API might return json string
import requests # to get the url
import datetime #get the timestamp right
import os # to access the os environment variables
import urllib2
import yahoo_finance
import pandas 
from pandas.io.data import DataReader #to work with such time series in Python

# make a printer
printer = pprint.PrettyPrinter()


# def timestamps():

# 	pass


# def get_historical_quotes():

# #self, start_date, end_date, ticker
# 	"""Return daily data for 3 years"""

# 	url = 'https://query.yahooapis.com/v1/yql?q=desc%20yahoo.finance.historicaldata&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='

# 	r = requests.get(url) #Request data 

# 	quotes = json.loads(json_string) #Convert JSON to Python dictionary

# 	pass




#ticker_df = pd.DataFrame(ticker_data)

#ticker_df.to_csv("/home/animesh/ticker_stock_data.csv")

def get_single_stock_data(ticker):

	"""get single stock data that takes in a single ticker symbol and returns a dictionary"""


	symbol = yahoo_finance.Share(ticker)
	past_date = datetime.datetime.now() - datetime.timedelta(days=3*365)
	str_past_date = datetime.datetime.strftime(past_date, "%Y-%m-%d")
	str_today_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
	ticker_data = symbol.get_historical(str_past_date, str_today_date)

	return {ticker : ticker_data}


def get_all_stock_data(tickers):
	""" takes in a list of ticker symbols and returns a dictionary of data"""

	
	historicaldata = []

	for ticker in tickers:

		this = get_single_stock_data(ticker)
		historicaldata.append(this)

	return historicaldata

		# add to dictionary

		# helper functions 

		# #routes later

if __name__=="__main__":

	test = get_all_stock_data(['GOOG', 'YHOO'])
	printer.pprint(test)


