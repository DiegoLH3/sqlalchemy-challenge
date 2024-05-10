# Import the dependencies.
import numpy as np
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(auotload_with= engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Hello_World():
    """List all of the available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():

    session = Session(engine)
    """Return a list of all percipitation and dates"""

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_percipitation = []
    for date,prcp in results:
        percipitation_dict = {}
        percipitation_dict[date] = prcp
        all_percipitation.append(percipitation_dict)

    return jsonify(all_percipitation)

@app.route('/api/v1.0/stations')
def stations():
    
    session = Session(engine)
    """Return a list of all stations"""
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_dict["Elevation"] = elevation
        all_stations.append(station_dict)



    return jsonify(all_stations)


@app.route('/api/v1.0/tobs')
def tobs():
    
    session = Session(engine)
    """Return a list of all temp. observations"""
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_names = [name[0] for name in results]

    return jsonify(all_names)


@app.route('/api/v1.0/start')
def start():

    session = Session(engine)
    """Return a list of all temp. observations"""
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_names = [name[0] for name in results]

    return jsonify(all_names)


@app.route('/api/v1.0/start/end')
def start_and_end():

    session = Session(engine)
    """Return a list of all temp. observations"""
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_names = [name[0] for name in results]

    return jsonify(all_names)


