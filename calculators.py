# Import libraries and functions
import math
import json
import requests
import io
import re
import numpy as np

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functions import apology


# Configure CS50 Library to use SQLite database for tracking COVID-19 cases on all campuses
db = SQL(os.getenv("postgres://lpfouuwaqafeui:07dcb40ce387e67e079db019402d7b051177ffe6df0dfbae8c1521669d4e3770@ec2-54-205-187-125.compute-1.amazonaws.com:5432/dd6so4du63g3gl"))

def calc_v1():

    # Check for required form entries
    if not request.form.get("positivity"):
        return apoligy("Please input positivity rate")

    if not request.form.get("length"):
        return apology("Please put your classroom length")

    if not request.form.get("width"):
        return apology("Please put your classroom width")

    if not request.form.get("height"):
        return apology("Please put your classroom height")

    if not request.form.get("time"):
        return apology("Please put your classroom time")

    if not request.form.get("students"):
        return apology("Please put the amount of students attending class")

    if not request.form.get("classes"):
        return apology("Please enter total number of classes per semester")

    # Update data assuming previous conditions are not met
    db.execute("BEGIN TRANSACTION")
    db.execute("UPDATE calculations SET  positivity = ?, length = ?, width = ?, height = ?, time = ?, students = ?",
        request.form.get("positivity"), request.form.get("length"), request.form.get("width"), request.form.get("height"),
        request.form.get("time"), request.form.get("students"))

    if request.form.get("airex"):
        db.execute("UPDATE calculations SET air_exchange = ? WHERE positivity = ?", request.form.get("airex"), request.form.get("positivity"))
    else:
        db.execute("UPDATE calculations SET air_exchange = ? WHERE positivity = ?", 1.2, request.form.get("positivity")) # 1.2 air exchanges set as default for calculations

    if request.form.get("filtration"):
        db.execute("UPDATE calculations SET filtration_eff = ? WHERE positivity = ?", request.form.get("filtration"), request.form.get("positivity"))
    else:
        db.execute("UPDATE calculations SET filtration_eff = ? WHERE positivity = ?", 0.65, request.form.get("positivity")) # 0.65 set as default Mask Filtration Efficiency
    db.execute("COMMIT")

    # Probability Calculation START
    positivity = list(db.execute("SELECT positivity FROM calculations"))

    # Setting Variables
    length_ft = list(db.execute("SELECT length FROM calculations"))
    length_cm = float(length_ft[0]["length"]) * 30.48

    width_ft = list(db.execute("SELECT width FROM calculations"))
    width_cm = float(width_ft[0]["width"]) * 30.48

    height_ft = list(db.execute("SELECT height FROM calculations"))
    height_cm = float(height_ft[0]["height"]) * 30.48

    time = list(db.execute("SELECT time FROM calculations"))

    students = list(db.execute("SELECT students FROM calculations"))
    filtration_mask = list(db.execute("SELECT filtration_eff FROM calculations"))

    classes_num = request.form.get("classes")

    air_ex = list(db.execute("SELECT air_exchange FROM calculations"))

    # Actual Calculations
   Dmask = 1 - (float(filtration_mask[0]["filtration_eff"]))
    volume = (length_cm * width_cm * height_cm) / 1000

    infected = float(students[0]["students"]) * float(positivity[0]["positivity"])/100
    infected_exhaled = infected * 70 * Dmask
    time_min = float(time[0]["time"]) * 60
    n = infected_exhaled / volume

    Dhvac = math.exp((float(air_ex[0]["air_exchange"]) * -1 * float(time_min) / 60))

    time_list = list(range(0, int(time_min)))

    local_n = [0] * len(time_list)

    for minute in time_list:
        local_density = 0

        for i in range(0, minute):
            diff = time_list[minute] - i + 1
            dilution = math.exp((float(air_ex[0]["air_exchange"]) * -1 * diff) / 60)
            local_density = local_density + (n * dilution)

        local_n[minute] = local_density

    inhale = np.multiply(local_n, Dmask * (450/60))
    dose_class = np.sum(inhale)
    dose_sem = dose_class * float(classes_num)
    probability_whole = (1-math.exp(-dose_sem/100)) * 100
    probability = round(probability_whole, 4)
    db.execute("UPDATE calculations SET infection = ?", probability)

def calc_v2():

    # Check for required form entries
    if not request.form.get("positive") or not request.form.get("total"):
        return apology("Please input covid cases")

    if not request.form.get("length"):
        return apology("Please put your classroom length")

    if not request.form.get("width"):
        return apology("Please put your classroom width")

    if not request.form.get("height"):
        return apology("Please put your classroom height")

    if not request.form.get("time"):
        return apology("Please put your classroom time")

    if not request.form.get("students"):
        return apology("Please put the amount of students attending class")

    if not request.form.get("classes"):
        return apology("Please enter total number of classes per semester")

    # Update data if the previous conditions are not met
    positivity_rate = (request.form.get("positive") / request.form.get("total")) * 100

    db.execute("BEGIN TRANSACTION")
    db.execute("UPDATE calculations SET  positivity = ?, length = ?, width = ?, height = ?, time = ?, students = ?",
        positivity_rate, request.form.get("length"), request.form.get("width"), request.form.get("height"),
        request.form.get("time"), request.form.get("students"))

    if request.form.get("airex"):
        db.execute("UPDATE calculations SET air_exchange = ? WHERE positivity = ?", request.form.get("airex"), positivity_rate)
    else:
        db.execute("UPDATE calculations SET air_exchange = ? WHERE positivity = ?", 1.2, positivity_rate)
        # 1.2 ACPH is the default air exchange rate for our calculations

    if request.form.get("filtration"):
        db.execute("UPDATE calculations SET filtration_eff = ? WHERE positivity = ?", request.form.get("filtration"), positivity_rate)
    else:
        db.execute("UPDATE calculations SET filtration_eff = ? WHERE positivity = ?", 0.65, positivity_rate)
        # 0.65 is the default mask filtration rate for our calculations

    db.execute("COMMIT")

    # Probability Calculation START
    positivity = list(db.execute("SELECT positivity FROM calculations"))

    # Setting Variables
    length_ft = list(db.execute("SELECT length FROM calculations"))
    length_cm = float(length_ft[0]["length"]) * 30.48

    width_ft = list(db.execute("SELECT width FROM calculations"))
    width_cm = float(width_ft[0]["width"]) * 30.48

    height_ft = list(db.execute("SELECT height FROM calculations"))
    height_cm = float(height_ft[0]["height"]) * 30.48

    time = list(db.execute("SELECT time FROM calculations"))

    students = list(db.execute("SELECT students FROM calculations"))
    filtration_mask = list(db.execute("SELECT filtration_eff FROM calculations"))

    classes_num = request.form.get("classes")

    air_ex = list(db.execute("SELECT air_exchange FROM calculations"))

    # Actual Calculations
    Dmask = 1 - (float(filtration_mask[0]["filtration_eff"])
    volume = (length_cm * width_cm * height_cm) / 1000

    infected = float(students[0]["students"]) * float(positivity[0]["positivity"])/100
    infected_exhaled = infected * 70 * Dmask
    time_min = float(time[0]["time"]) * 60
    n = infected_exhaled / volume

    Dhvac = math.exp((float(air_ex[0]["air_exchange"]) * -1 * time_min) / 60)

    time_list = list(range(0, int(time_min)))

    local_n = [0] * len(time_list)

    for minute in time_list:
        local_density = 0

        for i in range(0, minute):
            diff = time_list[minute] - i + 1
            dilution = math.exp((float(air_ex[0]["air_exchange"]) * -1 * diff) / 60)
            local_density = local_density + (n * dilution)

        local_n[minute] = local_density

    inhale = np.multiply(local_n, Dmask * (450/60))
    dose_class = np.sum(inhale)
    dose_sem = dose_class * float(classes_num)
    probability_whole = (1-math.exp(-dose_sem/100)) * 100
    probability = round(probability_whole, 4)
    db.execute("UPDATE calculations SET infection = ?", probability)
