# Import libraries and functions
import time
import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, abort, url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functions import apology
from calculators import (calc_v1, calc_v2)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database for tracking COVID-19 cases on all campuses
db = SQL(os.getenv("postgres://lpfouuwaqafeui:07dcb40ce387e67e079db019402d7b051177ffe6df0dfbae8c1521669d4e3770@ec2-54-205-187-125.compute-1.amazonaws.com:5432/dd6so4du63g3gl"
))


@app.route("/")
def index():
    """Show Homepage tab"""

    # Render the homepage file
    return render_template("c19index.html")


@app.route("/calc")
def calculator():
    """Show Risk Calculator tab"""

    # Render the calculator containing the map file
    return render_template("c19calc.html")


@app.route("/policies")
def uni_policies():
    """Show Policies tab"""

    # Render the policies list
    return render_template("c19policies.html")


@app.route("/cdc")
def cdc():
    """Show CDC Guidelines tab"""

    # Render the CDC information
    return render_template("c19cdc.html")


@app.route("/probability", methods=["GET", "POST"])
def probability():
    """Show Infection Probability tab"""
    if request.method == "GET":

        # Select the stored infection rate from the database
        infection = db.execute("SELECT infection FROM calculations")[0]["infection"]

        # Render the calculator containing the map file
        return render_template("c19probability.html", infection=infection)

    else:
        return apology("Please use a college risk calculator")


@app.route("/browncalc", methods=["GET", "POST"])
def brown():
    """Show Brown calculator"""
    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render the infection probability if the form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/browncalc.html")


@app.route("/caltechcalc", methods=["GET", "POST"])
def caltech():
    """Show Caltech calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/caltechcalc.html")


@app.route("/colcalc", methods=["GET", "POST"])
def columbia():
    """Show Columbia calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render the infection probability if the form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/colcalc.html")


@app.route("/corncalc", methods=["GET", "POST"])
def cornell():
    """Show Cornell calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/corncalc.html")


@app.route("/dartcalc", methods=["GET", "POST"])
def Dartmouth():
    """Show Dartmouth calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/dartcalc.html")


@app.route("/dukecalc", methods=["GET", "POST"])
def duke():
    """Show Duke calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v2()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/dukecalc.html")


@app.route("/harvcalc", methods=["GET", "POST"])
def harvard():
    """Show Harvard calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render the infection probability if the form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("/colleges/harvcalc.html")


@app.route("/jhucalc", methods=["GET", "POST"])
def JohnsHopkins():
    """Show Johns Hopkins calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v2()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/jhucalc.html")


@app.route("/mitcalc", methods=["GET", "POST"])
def mit():
    """Show MITs calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render the infection probability if the form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/mitcalc.html")


@app.route("/nwcalc", methods=["GET", "POST"])
def northwestern():
    """Show Northwestern calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/nwcalc.html")


@app.route("/princecalc", methods=["GET", "POST"])
def princeton():
    """Show Princeton calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render the infection probability if the form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/princecalc.html")


@app.route("/ricecalc", methods=["GET", "POST"])
def rice():
    """Show Rice calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/ricecalc.html")


@app.route("/stanfcalc", methods=["GET", "POST"])
def stanford():
    """Show Stanford calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/stanfcalc.html")


@app.route("/uchiccalc", methods=["GET", "POST"])
def uchic():
    """Show UChicago calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/uchiccalc.html")


@app.route("/upenncalc", methods=["GET", "POST"])
def upenn():
    """Show UPenn calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/upenncalc.html")


@app.route("/vandycalc", methods=["GET", "POST"])
def vanderbilt():
    """Show Vandebilt calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/vandycalc.html")


@app.route("/washucalc", methods=["GET", "POST"])
def washu():
    """Show WashU calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v1()

        # Only render infection probability if this form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/washucalc.html")


@app.route("/yalecalc", methods=["GET", "POST"])
def yale():
    """Show Yales calculator"""

    if request.method == "POST":

        # Compute infection rate and check for required form entries
        calc_v2()

        # Only render the infection probability if the form is submitted
        return redirect("/probability", code=307)

    else:
        return render_template("colleges/yalecalc.html")


# Define error function
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
