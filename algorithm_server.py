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


CHARTJS_COLORS = ["#b366ff", "#0059b3", "#00cc99", "#ffd480",
               "#ff99cc", "#b3e6ff", "#bfff80", "#ffccb3"]

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

    stockstring = stocklist[0]
    for stock in stocklist[1:]:
        stockstring =  stockstring + "&" + stock
    g_values = {"gender":gender, "agegroup":agegroup, "income": income, "amounttoinvest": amounttoinvest, "riskexpectation":riskexpectation,"returnexpectation":returnexpectation}
    
    session["g_values"] = g_values


     # if len(stocklist)<2 or len(stocklist)>5:
        # flash("Please choose min 2 or max 5 symbols")
    if len(stocklist)>5:
        flash("Please choose 5 symbols")
        return redirect("/start")
    elif gender == "" or agegroup == "" or income == "" or amounttoinvest == "" or riskexpectation == "" or returnexpectation == "":
        flash("Kindly do not leave the choice blank!")
        return redirect("/start")
    else:
        flash("Successfully added the information.")

        return redirect("/list/%s" % stockstring)

    # we can use jquery ajax to highlight a field in red in case no input




#----------------------------------------------------------------------------

# SIMILAR TO BELOW ROUTE SHOW USER THE LIST OF STOCKS ADDED FOR ANALYSIS
@app.route("/list/<stockstring>")
def show_list(stockstring):
    """Show info of list of symbols selected"""

   
    stocklist = stockstring.split("&")
    symbol_info_list = []
    for symbol in stocklist:
        symbol_info = Stock.query.get(symbol)
        symbol_info_list.append(symbol_info)
        # print symbol_info_list
    g_values = session["g_values"]

    return render_template("user_list.html", symbol_info_list=symbol_info_list, g_values=g_values)




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
    
    final = optimization.final_portfolio(symbol_list)


    return render_template("results.html", symbol_list=symbol_list, final=final)
    # not sure of passing yahooapidata in render template
   
    # need to send the stocklist to yahoo_api.py and that data to optimization


@app.route("/final.json")
def stock_pie_data():
    """Return page with results of the stock pie allocation in form of a
    pie chart."""
 #ajax request , REQUEST.ARGS.GET (GET THE STOCKLIST OUT)

    # weights = results(final)
    weights = {'GOOG': 0.09984881968219586, 'YHOO': 0.29996987179127077, 'AAPL': 0.2999752441661823, 'AA': 0.2999938062886864, 
    'MSFT': 0.00021225807166471572}

    labels = set([]) # store the keys in the label set

    for key in weights:
        labels.add(key)

    data = []
    for value in weights:
        # print "value", value
        rounded_value = int(weights[value]*100)
        data.append(rounded_value)
        print data
 
   
    backgroundColors = CHARTJS_COLORS[:len(labels)]
    hoverBackgroundColors = CHARTJS_COLORS[:len(labels)]
 
    #  [0.0998488196821958, 0.29996987179127077, 0.2999752441661823, 0.2999938062886864, 0.00021225807166471572]   
 
    data_list_of_dicts = {

                    "labels": list(labels),
                    "datasets":[{"data": data,
                    "backgroundColor": backgroundColors,
                    "hoverBackgroundColor": hoverBackgroundColors}]
                    }

                    
    print data_list_of_dicts 
    return jsonify(data_list_of_dicts)

    #----------------------------------------------------------------------------------------------

@app.route("/test")
def test_results():


    return render_template("test_chart.html")


















if __name__ == "__main__":
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)

