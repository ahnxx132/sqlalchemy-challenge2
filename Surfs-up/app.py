import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# Reflect an existing database into a new model.
Base = automap_base()
# Reflect the tables.
Base.prepare(engine, reflect=True)

# Save reference to the tables.
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__,static_url_path='/Images/surfs-up.png')


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h1>Welcome to the Climate APP API!</h1>"
        f"<h2>Part 2 - Climate App</h2>"
        f" <img width='600' src='https://www.travelalerts.ca/wp-content/uploads/2018/05/shutterstock_145257634.jpg'/ >"
        f"<h2>Here are the available routes:</h2>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
       
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query to retrieve the last 12 months of precipitation data and return the results."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

# Find the most recent date in the data set.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #converting to tuple
    (last_date, ) = last_date
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    last_date = last_date.date()
    one_year_date = last_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores.
    last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers.
    precipitation = []
    for date, prcp in last_year:
        precipitation_dict = {}
        #using date as the key and prcp as the value.
        precipitation_dict[date] = prcp
        # precipitation_dict['prcp'] = prcp
        precipitation.append(precipitation_dict)

    # Return the JSON representation of dictionary.
    return jsonify(precipitation)


@app.route("/api/v1.0/tobs")
def tobs():
    """Query for the dates and temperature observations from a year from the last data point for the most active station."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Find the most recent date in the data set.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #converting to tuple
    (last_date, ) = last_date
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    last_date = last_date.date()
    one_year_date = last_date - dt.timedelta(days=365)

    # Find the most active station.
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()

    # Get the station id of the most active station. making it into tuple
    (most_active_station_id, ) = most_active_station

    # Perform a query to retrieve the data and temperature scores for the most active station from the last year.
    last_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= one_year_date).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and temperature as the value.
    all_temperatures = []
    for date, temp in last_year:
        temp_dict = {}
        temp_dict[date] = temp
        all_temperatures.append(temp_dict)
    # Return the JSON representation of dictionary.
    return jsonify(all_temperatures)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for stations.
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Convert the query results to a dictionary.
    all_stations = []
    for station, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    # Return the JSON representation of dictionary.
    return jsonify(all_stations)


@app.route('/api/v1.0/<start>', defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def rangestartend(start,end=None):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date (inclusive)."""
    # Create our session (link) from Python to the DB
    session = Session(engine)



if __name__ == '__main__':
    app.run(debug=True)