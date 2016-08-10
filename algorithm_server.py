"""Optimization application Flask server.

Provides web interface for stock allocation.

Authors: Madhuri Ghosh.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2


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



@app.route("/stocks")
def 


















if __name__ == "__main__":
    app.run(debug=True)


	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run()