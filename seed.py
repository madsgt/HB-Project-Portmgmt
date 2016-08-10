"""Utility file to seed stockportfolio database from stocks and favorites data in seed_data/"""

import datetime
import sqlalchemy

from data_model import Stock, Favorite, connect_to_db, db

from algorith_server import app


def load_stocks():
	"""Load stocks from S&P500constituents.csv into database."""

	print "Stocks"

	for i, row in enumerate(open("seed_data/S&P500constituents.csv")):
		row = row.rstrip()
		symbol, name, sector = row.split(",")

		stock = Stock(symbol=symbol, name=name, sector=sector)

		db.session.add(user) # add to the session for storing

	db.session.commit()


def load_favorites():

	"""Load counter + symbols from user clicks into database, keep the counter ticking"""

	print "Favorites"

	# Need help on this, create dummy data

	for i, row in enumerate(open())







if __name__ == "__main__":
	connect_to_db(app)
    db.create_all()


    Stock.query.delete() 

    load_stocks()
    load_favorites()