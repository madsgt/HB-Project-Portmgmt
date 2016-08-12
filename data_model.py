"""Model and database functions for Stock portfolio allocation project."""

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting this through  
# the Flask-SQLAlchemy helper library. On this, we can find the `session`  
# object, where we do most of our interactions (like committing, etc.)  

db = SQLAlchemy()

#Model definition-

class Stock(db.Model):  
   """Stocks in S&P500"""  

   __tablename__ = "stocks"  
 
	symbol = db.Column(db.String(6), nullable=False, primary_key=True) 
  name = db.Column(db.String(42), nullable=False) 
  sector = db.Column(db.String(30), nullable=False) 
		 

 
	def __repr__(self): 
        """Provide helpful representation when printed.""" 
       return "<Stock ticker=%s name=%s>" % (self.symbol, self.name) 


#--------------------------------------------------------------------------------------------
# havent made a model for data from yahoo_API.py , butI dont want to store the information ,it will 
# keep refreshing every time user comes to the site. unless symbol repeated within a day,
# delete the db at the end of the day, 
#2.scheduling yr api run at the beginning of day for all stocks in the list
#and delete at end of day or
# option 3- delete one day and add one day and refresh db (difference), can do later

class YahooData(db.Model):
  """data from yahoo finance API, need the close price and the market cap for the symbol
  data expected is 3 yrs daily prices and mcap realtime only once"""
  #??? Can I pick only 2 data points from complete data 

  __tablename__ = "yahoodata"

  symbol = db.Column(db.String(6), db.ForeignKey('stocks.symbol'), nullable=False)
  adj_close = db.Column(db.String(6), nullable=True)
  market_cap = db.Column(db.String(50), nullable=True) # mcap shows as '1.25B'

  stock = db.relationship('Stock', backref='yahoodata')


  def __repr__(self): 
        """Provide helpful representation when printed.""" 
       return "Stock ticker=%s Close Price=%s Market Cap=%s>" % (self.symbol, self.adj_close, self.market_cap)

#--------------------------------------------------------------------------------------------

#to be done later

# class Favorite(db.Model):
# 	"""TO store the counter for clicks or choice of top 5 stocks of all time against the tickers and display the top\
# 	\5 tickers to users"""

# 	__tablename__ = "favorites"

# 	id = db.Column(db.Column(db.Integer, primary_key=True)
# 	symbol = db.Column(db.String(6), db.ForeignKey('stocks.symbol'), nullable=False)
# 	counter = db.Column(db.Integer, nullable=True, default=0)


# 	stock = db.relationship('Stock', backref='favorites', order_by=desc(counter))


# 	def __repr__(self): 
#     """Provide helpful representation when printed.""" 
#    		return "Stock ticker=%s counter=%s>" % (self.symbol, self.counter) 

    
















##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stockportfolio'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

     




