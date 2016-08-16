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

@app.route("/tickers")


# Similar to below show list of stocks to select from by way of dropdown or 
# autocomplete
@app.route("/start")
def user_data():
#     """Return page showing text box with list of stocks to choose from a dropdown or autocomplete """

    stocks_list = Stock.get_all()
    return render_template("useractivity_capture.html",
                           stocks_list=stocks_list)
    # or return redirect("/useractivity_capture.html")
    pass
#-----------------------------------------------------------------------------------------------

# SIMILAR TO BELOW ROUTE SHOW USER THE LIST OF STOCKS ADDED FOR ANALYSIS
@app.route("/list")
def add_to_list():

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

#     return render_template("user_list.html", stock_list=stock_list, stock_total=stock_total)

    pass

#--------------------------------------------------------------------------------

@app.route("/add_to_list/<string:symbol>")
def add_to_list(symbol):
    """Add a stock to list and redirect to user_list.html.

    # When a stock is added to the list, redirect browser to the user_list
    # page and display a confirmation message: 'Successfully added to list'.
    # """

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
    return render_template("results.html")
     


@app.route("/final.json")
def stock_pie_data():
    """Return data about the stocks."""

    data_list_of_dicts = {

    # Need to add infor from calculations of weights from Optimization.py file
        # 'stocks': [
        #     {
        #         "value": 300,
        #         "color": "#F7464A",
        #         "highlight": "#FF5A5E",
        #         "label": "Christmas Melon"
        #     },
        #     {
        #         "value": 50,
        #         "color": "#46BFBD",
        #         "highlight": "#5AD3D1",
        #         "label": "Crenshaw"
        #     },
        #     {
        #         "value": 100,
        #         "color": "#FDB45C",
        #         "highlight": "#FFC870",
        #         "label": "Yellow Watermelon"
            }

    pass
# return jsonify(data_list_of_dicts)


















if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


connect_to_db(app)

    # Use the DebugToolbar
DebugToolbarExtension(app)

app.run()