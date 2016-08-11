"""Optimization application Flask server.

Provides web interface for stock allocation.

Authors: Madhuri Ghosh.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2
import optimization


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")



@app.route("/start")
def user_data():
	"""process the user data and store it"""

	# need to capture data from form that user enters and store it in db w/o logging in ,use of Javascript
	#capture submit

	return redirect("/useractivity_capture.html")



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