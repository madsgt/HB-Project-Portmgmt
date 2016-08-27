"""Model and database functions for Stock portfolio allocation project."""

from flask_sqlalchemy import SQLAlchemy
import optimization


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
        return "<Stock ticker=%s name=%s sector=%s>" % (self.symbol, self.name, self.sector) 


#--------------------------------------------------------------------------------------------
# havent made a model for data from yahoo_API.py , butI dont want to store the information ,it will 
# keep refreshing every time user comes to the site. unless symbol repeated within a day,
# delete the db at the end of the day, 
#2.scheduling yr api run at the beginning of day for all stocks in the list
#and delete at end of day or
# option 3- delete one day and add one day and refresh db (difference), can do later

class YahooData(db.Model):
    """data from yahoo finance API, need the adj_close price for the symbol
    data expected is 3 yrs daily prices"""
    #??? Can I pick only 2 data points from complete data 

    __tablename__ = "yahoodata"

    data_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String(6), db.ForeignKey('stocks.symbol'))
    adj_close = db.Column(db.String(6), nullable=False)
    # market_cap = db.Column(db.String(50), nullable=True) # mcap shows as '1.25B'

    stock = db.relationship('Stock', backref='yahoodata')


    def __repr__(self): 
        """Provide helpful representation when printed.""" 
        return "<Stock ticker=%s Close Price=%s>" % (self.symbol, self.adj_close)

#--------------------------------------------------------------------------------------------

# the class below has no relationship with the classes above, it is abt form inputs from html

class UserData(db.Model):
    """User data from the form inputs stored in this form"""

    __tablename__ = "userdata"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    gender = db.Column(db.String(50), nullable=False)
    agegroup = db.Column(db.String(50), nullable=False)
    income = db.Column(db.String(50), nullable=False)
    amounttoinvest = db.Column(db.String(50), nullable=False)
    riskexpectation = db.Column(db.String(50), nullable=False)
    returnexpectation = db.Column(db.String(50), nullable=False)


    def __repr__(self): 
        """Provide helpful representation when printed.""" 
        return "<user_id=%s gender=%s agegroup=%s income=%s amounttoinvest=%s riskexpectation=%s returnexpectation=%s>" % (self.user_id, self.gender, self.agegroup, self.income, self.amounttoinvest, self.riskexpectation, self.returnexpectation)

#--------------------------------------------------------------------------------------------
class Favorite(db.Model):
    """User inputs for favorite symbols from the form inputs stored here and counter created"""

    __tablename__ = "favorites"

    favorites_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String(6), db.ForeignKey('stocks.symbol'))
    counter = db.Column(db.Integer, nullable=True, default=1)#fixme need to calculate if symbol already in db increment by one the same row

    stock = db.relationship('Stock', backref='favorites', order_by='desc(Favorite.counter)')

    def favoritestock(self):

        self.counter += 1
        db.session.commit()




    
    def __repr__(self): 
        return "<favorites_id=%s symbol=%s name=%s sector=%s counter=%s>" % (self.favorites_id, self.symbol, self.name, self.sector, self.count.counter)         

# def example_data():
#     """Create some sample data."""

#     # In case this is run more than once, empty out existing data
#     Stock.query.delete()
#     UserData.query.delete()
#     YahooData.query.delete()      

#     # Add sample stocks and yahoodata and userdata
#     stock1 = Stock(symbol='ACZ', name='ACUTEIZ', sector='Utilities')
#   
#     ezra = UserData(name='Leonard', dept=dl)
#     
#     nadine = Employee(name='Nadine')

#     db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
#     db.session.commit()




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stockportfolio'
    app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from algorithm_server import app
    connect_to_db(app)
    print "Connected to DB."
