"""Optimization application Flask server.

Provides web interface for stock allocation.

Authors: Madhuri Ghosh.
"""

from flask import Flask, render_template, redirect, flash, session, request, jsonify, make_response, g
import jinja2
import optimization
import yahoo_api
import json
from data_model import Stock, YahooData, UserData, Favorite, UserFavorite, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc

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

  
    symbol_data = Favorite.query.order_by(desc(Favorite.counter)).limit(5).all()
    userfavdata = UserFavorite.query.all() #added on 3st aug
    # need to create charts of individual userinfo

     
    return render_template("homepage.html", symbol_data=symbol_data, userfavdata=userfavdata)

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

    symbols = request.form.getlist('symbol')
    g.symbols = symbols 
    session["symbols"] = symbols 

    gender = request.form.get('gender')
    agegroup = request.form.get('agegroup')
    income = request.form.get('income')
    amounttoinvest = request.form.get('amounttoinvest')
    riskexpectation = request.form.get('riskexpectation')
    returnexpectation = request.form.get('returnexpectation')

    print symbols
    print "I am server related"

    userdata = UserData(gender=gender, agegroup=agegroup, income=income, 
        amounttoinvest=amounttoinvest, riskexpectation=riskexpectation, 
        returnexpectation=returnexpectation) 

    #loops over each symbol to check fovarites table,if present we increase counter else add the symbol and counter to the table in not present
    for symbol in symbols: 
        check = Favorite.query.filter_by(symbol=symbol).first()
        if check:
            check.counter +=1
        else:
            favorite = Favorite(symbol=symbol)
            db.session.add(favorite)

        userfavorite = UserFavorite(favorites_id = favorites.favorites_id, user_id=userdata.user_id) #added on 31st aug
            

    db.session.add(userdata)  # add to the session for storing
    db.session.add(userfavorite) #added 31 Aug

    db.session.commit()
    
    final = optimization.final_portfolio(symbols) #from symbols to symbol_list
    print final
    print "I am server related"


    return render_template("results.html", symbol_list=symbols, final=final, symbols=symbols) # 30-aug addition tickers
    # put in html using jinja and hide it and select using use ajac to send data to next route
    # not sure of passing yahooapidata in render template
   
    # need to send the stocklist to yahoo_api.py and that data to optimization


@app.route("/final.json")
def stock_pie_data():
    """Return page with results of the stock pie allocation in form of a
    pie chart."""
#  #ajax request , REQUEST.ARGS.GET (GET THE STOCKLIST OUT)
#     #use session
        
    symbols = session["symbols"] # 30-aug addition
    # symbols = request.form.getlist('symbol')
    weights = optimization.final_portfolio(symbols) # 30-aug addition

#     # weights = {'GOOG': 0.09984881968219586, 'YHOO': 0.29996987179127077, 'AAPL': 0.2999752441661823, 'AA': 0.2999938062886864, 
#     # 'MSFT': 0.00021225807166471572}

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

# @app.route("/test")
# def test_results():


#     return render_template("test_chart.html")




if __name__ == "__main__":
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", debug=True)

