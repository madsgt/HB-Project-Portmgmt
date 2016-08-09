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
 
		ticker = db.Column(db.String(6), nullable=False, primary_key=True) 
	   	name = db.Column(db.String(42), nullable=False) 
	   	sector = db.Column(db.String(30), nullable=False) 
		industry = db.Column(db.String(56), nullable=False) 

 

	def __repr__(self): 
        """Provide helpful representation when printed.""" 
       return "Stock ticker=%s name=%s>" % (self.ticker, self.name) 
     




