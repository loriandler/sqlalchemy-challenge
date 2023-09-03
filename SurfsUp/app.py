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
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

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
#################################################
# Define the home route

@app.route("/")
def welcome():
    return (
        "Hawaii Weather Data: Available routes:\n"
        "/api/v1.0/preciptation\n"
        "/api/v1.0/stations\n"
        "/api/v1.0/tobs\n"
        "/api/v1.0/<start>\n"
        "/api/v1.0/<start>/<end>"
    )

# Define the participation route
@app.route("/api/v1.0/precipitation")
def get_precipitation():
    # Calculate one year ago from the most recent date
    start_date = '2016-08-23'
    sel = [measurement.date, func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
        filter(measurement.date >= start_date).\
        group_by(measurement.date).\
        order_by(measurement.date).all()
    
    # Convert query results to dictionary
    precipitation_dates = []
    precipitation_totals = []

    for date, total in precipitation:
        precipitation_dates.append(date)
        precipitation_totals.append(total)
    
    precipitation_dict = dict(precipitation_dates, precipitation_totals)

    
    return jsonify(precipitation_dict)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    sel = [mesaurement.station]
    active = session.query(*sel).\
        group_by(measurement.station).all()
    
    list_of_stations = list(np.ravel(active))
    return jsonify(list_of_stations)
    

# # Define the temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():

    start_date = '2016-08-23'
    sel = [measurement.date, measurement.tobs]
    temps = session.query(*sel).\
        filter(measurement.date >= start_date, measurement.station == 'USC00519281').\
        group_by(measurement.date).\
        order_by(measurement.date).all()

# Extract temperature values from the query results
observation_dates = []
temp_observe = []

for date, observation in temps:
    observation_dates.append(date)
    temp_observe.append(observation)

tobs_dict = dict(observation_dates, temp_observe)

return jsonify(tobs_dict)

# Define the temperature summary route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_summary(start_date, end=None):

    
    query_result = session.query(
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()


    #create dictionary list
    temp_stats = []

    for min_temp, avg_temp, max_temp in query_result:
        temp_dict = {
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "TempMIN": min_temp,
            "TempAVG": avg_temp,
            "TempMAX": max_temp
        }
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)

session.close()

if __name__ == '__main__':
    app.run(debug=True)





    