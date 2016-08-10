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
       return "Stock ticker=%s name=%s>" % (self.symbol, self.name) 






class Favorite(db.Model):
	"""TO store the counter for clicks or choice of top 5 stocks of all time against the tickers and display the top\
	\5 tickers to users"""

	__tablename__ = "favorites"

	id = db.Column(db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(6), db.ForeignKey('stocks.symbol'), nullable=False)
	counter = db.Column(db.Integer, nullable=True, default=0)


	stock = db.relationship('Stock', backref='favorites', order_by=desc(counter))


	def __repr__(self): 
    """Provide helpful representation when printed.""" 
   		return "Stock ticker=%s counter=%s>" % (self.symbol, self.counter) 

    
    # db_create_all















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

     




