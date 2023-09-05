# Import the dependencies.
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, jsonify
from datetime import datetime, timedelta
import pandas as pd

#################################################
# Database Setup
#################################################
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


# reflect an existing database into a new model
Base = automap_base()
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
############################

# Define the home routes

@app.route("/")
def welcome():
    return (
        f"<h1><b> Hawaii Weather Data </b></h1>"
        f"<h2><b> Available routes:</b></h2> </br>"
        f"<b> Precipitation Data: </b> /api/v1.0/precipitation </br>"
        f"<b> Observed Stations: </b> /api/v1.0/stations </br>"
        f"<b> Temperature Observations: </b> /api/v1.0/tobs </br>"
        f"<b> Temperature data for a specific date (add date YYYY-MM-DD):</b> /api/v1.0/<start> </br>"
        f"<b> Temperature data fo a range of dates (add start and end dates YYYY-MM-DD/YYYY-MM-DD): </b> /api/v1.0/<start><end>"
    )

# Define the participation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate one year ago from the most recent date
    # Starting from the most recent data point in the database. 
    most_recent_date_str = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    most_recent_date = datetime.strptime(most_recent_date_str, '%Y-%m-%d')

# Calculate the date one year from the last date in data set.
    one_yr_ago = most_recent_date - timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_yr_ago).\
        order_by(measurement.date).all()  

    session.close()  
    
# Convert query results to dictionary
    precipitation_dates = []
    precipitation_totals = []

    for date, total in results:
        precipitation_dates.append(date)
        precipitation_totals.append(total)
    
    precipitation_dict = dict(zip(precipitation_dates, precipitation_totals))

 # jsonify the results
    return jsonify(precipitation_dict)


# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

# Query the station names  
    stations = session.query(station.name, station.station).all()
    
    session.close()

# create list of stations
    station_list = [{"name": name, "station": station} for name, station in stations]

# jsnoify the results    
    return jsonify(station_list)
    

# # Define the temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

#Query the temperature observations (tobs)    
    temps = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == 'USC00519281').\
        all()

    session.close()

# Extract temperature values from the query results
    observation_dates = []
    temp_observe = []

    for date, observation in temps:
        observation_dates.append(date)
        temp_observe.append(observation)

        tobs_dict = dict(zip(observation_dates, temp_observe))

# jsonify the results
        return jsonify(tobs_dict)


# Define the temperature summary route for a particular date
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    results = (session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
               filter(measurement.date >= start).\
               all()
               )

# create list of the temperatures    
    (min, max, avg) = results[0]

    session.close()

# jsnoify the results
    return jsonify(f"Start date: {start}", f"Lowest Temperature: {min} degrees F", f"Highest Temperature:  {max} degrees F", f"Average Temperature: {avg} degrees F")

# Define the summaries for start and end dates
@app.route("/api/v1.0/<start>/<end>")
def temp_summary(start, end):
    session = Session(engine)
    

# query the max, min, avg temperature observations
    query_result = session.query(
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).\
            all()


#create dictionary list
    (min, avg, max) = query_result[0]

    session.close()

#jsnoify the results
    return jsonify(f"Start date: {start}", 
                   f"End date: {end}", 
                   f"Lowest Temperature: {min} degrees F", f"Highest Temperature: {max} degrees F", f"Average Temperature: {avg} degrees F")

# end the flask code
if __name__ == '__main__':
    app.run(debug=True)
