"""Optimization application Flask server.

Provides web interface for stock allocation.

Authors: Madhuri Ghosh.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
import optimization
import seed
import yahoo_api
import json


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined
app.jinja_env.auto_reload = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")

#-------------------------------------------------------------------------

# Similar to below show list of stocks to select from by way of dropdown or 
# autocomplete, need help to get the tickers thru d json
@app.route('/start', methods=['GET'])
def user_form():
    """Show form for user to fill in details."""
    
        return render_template("useractivity_capture.html")


@app.route('/start', methods=['POST'])
def user_data():
"""Return page showing text box with list of stocks to choose from a dropdown
or autocomplete """
    
    stocklist = request.form.getlist('stocklist')
    gender = request.form.getlist('gender')
    agegroup = request.form.getlist('agegroup')
    income = request.form.getlist('income')
    amounttoinvest = request.form.getlist('amounttoinvest')
    riskexpectation = request.form.getlist('riskexpectation')
    returnexpectation = request.form.getlist('returnexpectation')

    stockstring =""
    for stock in stocklist:
        stockstring = stockstring + stock + "&"


    if len(stocklist)<2 or len(stocklist)>5:
        flash("Please choose min 2 or max 5 symbols")
        return redirect("/start")
    else:
        flash("Successfully added the stocks.")
        return redirect("/list/%s" % stockstring)



 
#----------------------------------------------------------------------------

# SIMILAR TO BELOW ROUTE SHOW USER THE LIST OF STOCKS ADDED FOR ANALYSIS
@app.route("/list/<stockstring>")
def show_list(stocklist):
    """Show info of list of symbols selected"""

    stocklist = stockstring.split("&")
    symbol_info_list =[]
    for symbol in stocklist:
        symbol_info = Stock.query.get(symbol)
        symbol_info_list.append(symbol_info)
        print symbol_info
   

        
    return render_template("user_list.html", symbol_info_list=symbol_info_list)


#     """Add the list of stocks and display the information."""

#     stock_total = 0

#     # Get the stock_list (or an empty list if there's no stock_list yet)
#     add_stocks = session.get('stock_list', [])

#     # We'll use this dictionary to keep track of the symbols
#     # we have in the stock_list.
#     #
#     # Format: symbol -> {dictionary-of-stock_list-info}

#     stock_list = {}

#     # Loop over the symbols in the session stock_list to build up the
#     # `stock_list` dictionary

#     for symbol in add_stocks:

#         if symbol in stock_list:
#             stock_list_info = stock_list[symbol]= {
#                 'symbol': ccccccc.symbol,
#                 'count': 0,
#                   }

#         # increase  stock-total count
#         stock_list_info['stock_total'] += 1
#      
#     # Get the melon-info dictionaries from our cart
#     stock_list = stock_list.values()

#     return render_template("user_list.html", stock_list=stock_list, stock_
    # total=stock_total)



#--------------------------------------------------------------------------------

# @app.route("/add_to_list/<string:symbol>")
# def add_to_list(symbol):
#     """Add a stock to list and redirect to user_list.html.

#     # When a stock is added to the list, redirect browser to the user_list
#     # page and display a confirmation message: 'Successfully added to list'.
#     # """

    # # Check if we have a stock_list in the session dictionary and, if not, add one
    # if 'stock_list' in session:
    #     stock_list = session['stock_list']

    # else:
    #     stock_list = session['stock_list'] = []

    # # Add stock to stock_list
    # stock_list.append(symbol)

    # # Show user success message on next page load
    # flash("Successfully added to list.")

    # # Redirect to shopping cart page
    # return redirect("/list")

    pass

#------------------------------------------------------------------------------------   



@app.route("/final")
def results():
    """Return page with results of the stock pie allocation in form of a pie chart"""
    """ get stocklist out of the form and send stocklist to results.html"""

    # request.form.getlist()



    
    return render_template("results.html", stocklist=stocklist)

   
     


@app.route("/final.json")
def stock_pie_data():
    """Return data about the stocks."""
 #ajax request , REQUEST.ARGS.GET (GET THE STOCKLIST OUT)

    get_all_stock_data(stocklist)
    optimal_portfolio(returns)
    # the weights will be a list and make it a dictionary and 
    data_list_of_dicts = {
    # use for loop later to pick up 2 upto 5 symbols
    # 
    # Need to add infor from calculations of weights from Optimization.py file
        # 'stocks': [
        #     {
        #         "value": 15,
        #         "color": "#F7464A",
        #         "highlight": "#FF5A5E",
        #         "label": symbol1
        #     },
        #     {
        #         "value": 50,
        #         "color": "#46BFBD",
        #         "highlight": "#5AD3D1",
        #         "label": symbol2
        #     },
        #     {
        #         "value": 100,
        #         "color": "#FDB45C",
        #         "highlight": "#FFC870",
        #         "label": "Yellow Watermelon"
            }

    pass
# return jsonify(data_list_of_dicts)

# DATA_LIST_OF_DICTS GETS PASSED IN DATA IN js


















if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


connect_to_db(app)

    # Use the DebugToolbar
DebugToolbarExtension(app)

app.run()