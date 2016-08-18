"""Optimization application Flask server.

Provides web interface for stock allocation.

Authors: Madhuri Ghosh.
"""

from flask import Flask, render_template, redirect, flash, session, request, jsonify, make_response, g
import jinja2

import optimization
import yahoo_api
import json
from data_model import Stock, YahooData, UserData, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension

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
    """Return page showing text box with list of stocks to choose from a 
    dropdown or autocomplete."""

    stocklist = request.form.getlist('stocklist')
    gender = request.form.get('gender')
    agegroup = request.form.get('agegroup')
    income = request.form.get('income')
    amounttoinvest = request.form.get('amounttoinvest')
    riskexpectation = request.form.get('riskexpectation')
    returnexpectation = request.form.get('returnexpectation')
    g.gender = gender
    g.agegroup = agegroup
    g.income = income
    g.amounttoinvest = amounttoinvest
    g.riskexpectation = riskexpectation
    g.returnexpectation = returnexpectation

    stockstring =""
    for stock in stocklist:
        stockstring = stockstring + stock + "&"


    if len(stocklist)<2 or len(stocklist)>5:
        flash("Please choose min 2 or max 5 symbols")
        return redirect("/start")
    else:
        flash("Successfully added the information.")

        return redirect("/list/%s" % stockstring)





#----------------------------------------------------------------------------

# SIMILAR TO BELOW ROUTE SHOW USER THE LIST OF STOCKS ADDED FOR ANALYSIS
@app.route("/list/<stockstring>")
def show_list(stocklist):
    """Show info of list of symbols selected"""

    stocklist = stockstring.split("&")
    symbol_info_list = []
    for symbol in stocklist:
        symbol_info = Stock.query.get(symbol)
        symbol_info_list.append(symbol_info)
        print symbol_info_list

    return render_template("user_list.html", symbol_info_list=symbol_info_list)




@app.route("/final", methods=["POST"])
def results():
    """ get stocklist out of the form and send stocklist to results.html"""

    # request.form.getlist()
    symbol_list = []
    symbol = request.form.get('symbol')
    symbol_list.append(symbol)
    gender = request.form.get('gender')
    agegroup = request.form.get('agegroup')
    income = request.form.get('income')
    amounttoinvest = request.form.get('amounttoinvest')
    riskexpectation = request.form.get('riskexpectation')
    returnexpectation = request.form.get('returnexpectation')

    userdata = UserData(gender=gender, agegroup=agegroup, income=income, 
        amounttoinvest=amounttoinvest, riskexpectation=riskexpectation, 
        returnexpectation=returnexpectation)
    db.session.add(userdata) # add to the session for storing

    db.session.commit()

    yahooapidata = get_all_stock_data(symbol_list)
    
    return render_template("results.html", symbol_list=symbol_list)

   
    # need to send the stocklist to yahoo_api.py and that data to optimization


@app.route("/final.json")
def stock_pie_data():
    """Return page with results of the stock pie allocation in form of a
    pie chart."""
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