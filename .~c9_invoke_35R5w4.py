import os
import datetime
import pandas as pd
import requests
import io
import sqlalchemy

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from bs4 import BeautifulSoup
from functions import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database for tracking COVID-19 cases on all campuses
engine = sqlalchemy.create_engine("sqlite:///unicases.db")
data = requests.get("https://raw.githubusercontent.com/nytimes/covid-19-data/master/colleges/colleges.csv").content
df = pd.read_csv(io.StringIO(data.decode('utf-8')))
df.to_sql('unicases', con=engine, schema=None, if_exists="replace", index=None,
    dtype={'date': sqlalchemy.types.Text(), 'state': sqlalchemy.types.Text(), "county": sqlalchemy.types.Text(),
    "city": sqlalchemy.types.Text(), "ipeds_id": sqlalchemy.types.Integer(), "college": sqlalchemy.types.Text(),
    "cases": sqlalchemy.types.Integer(), "notes": sqlalchemy.types.Text()}) # Column types required specification
db = SQL("sqlite:///unicases.db")


@app.route("/")
def index():
    """Show site homepage"""

    # Render the homepage file
    return render_template("c19index.html")


# Extract positivity rate from Harvard dashboard
harvard = requests.get("https://www.harvard.edu/coronavirus/harvard-university-wide-covid-19-testing-dashboard#note")
soup = BeautifulSoup(harvard.text,'html.parser')

links = soup.find_all('a')
for link in links:
    link.decompose()

superscript = soup.find_all('sup')
for script in superscript:
    script.decompose()

harvard_rates = soup.find_all('h1')
positivity = harvard_rates[4]
positivity_element = positivity.contents
# Convert positivity rate from a list of strings to a float value for calculations
positivity_str = ''.join(map(str, positivity_element))
positivity_str = positivity_str[:-1] # Needed to remove the '%' symbol
harv_positivity_rate = float(positivity_str)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)