"""Utility file to seed stockportfolio database from stocks and favorites data in seed_data/"""

import datetime
import sqlalchemy

from data_model import Stock, YahooData, UserData, connect_to_db, db

from algorithm_server import app


def load_stocks():
	"""Load stocks from S&P500constituents.csv into database."""

	print "Stocks"

	for i, row in enumerate(open("seed_data/S&P500constituents.csv")):
		row = row.rstrip()
		symbol, name, sector = row.split(",")

		stock = Stock(symbol=symbol, name=name, sector=sector)

		db.session.add(stock) # add to the session for storing

	db.session.commit()



# def get_tickers():    
#     data = json.load(open("seed_data/S&P500constituents.json"))    
#     symbol, name, sector = data    
#     return json.dumps(data)

#-------------------------------------------------------------

def load_all_stock_data():


	pass
	# we need to load and store the api data some where to extract 
	# data is not is json or csv so how to load it 



#	---------------------------------------------------------------------

def load_favorites():

	# """Load counter + symbols from user clicks into database, keep the counter ticking"""

	# print "Favorites"

	# # Need help on this, created dummy data, how will I create the counter, as user clicks the counter adds

	# for i, row in enumerate(open("seed_data/dummy_clicks.csv")):
	# 	row = row.rstrip()
	# 	symbol, counter = row.split(",")

	# 	counter = Favorite(symbol=symbol, counter=counter)
	# 	db.session.add(counter)

	# db.session.commit()

	pass






if __name__ == "__main__":
	connect_to_db(app)

	db.create_all()

	Stock.query.delete() 

	load_stocks()
	load_favorites()