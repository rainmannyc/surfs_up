# Importing dependencies

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#   Importing Flask with jsonify (jsonify is a function that converts a dictionary to a JSON file)
from flask import Flask, jsonify

#   Creating a connection via engine to our sqlite database file
engine = create_engine("sqlite:///hawaii.sqlite")

#   Creating our foundation base via automap_base() function
Base = automap_base()

#   Reflecting our database into the foundation via engine 
Base.prepare(engine, reflect=True)

#   From using Base.class.keys() we know there are two classes, Measurement and Station.
#   In which now we will set the variables for below:

Measurement = Base.classes.measurement
Station = Base.classes.station

#   Creating a sessionl ink from Python to our database:
session = Session(engine)

#   Creating a Flask application called "app"
app = Flask(__name__)
#   Creating/Setting up our app "root"
@app.route("/")
#   Creating a function "welcome()" with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#   Generating the precipitation route
@app.route("/api/v1.0/precipitation")
# Creating a function to session query for the Measurement date and
# measurement precipitation, filtering the data to the date of the previous year(prev_year)
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#   Generating a route for the "stations"
@app.route("/api/v1.0/stations")
#   Creating a function to get all the stations in our database
#   We are also using the function 'np.ravel' with "results" in our parameters
#   while converting the array to a list with list():
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
    

#   Generating a temperature observation route, filtering by specific station and tracing back 1 year ago.
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#   Generating a function 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=2017-6-1, end=2017-6-30):
    #Creating a list called "sel"
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results)) 
        return jsonify(temps)

    results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)