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

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
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
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)



    return jsonify(all_stations)


@app.route('/api/v1.0/tobs')
def tobs():
    
    session = Session(engine)
    """Return a list of all temp. observations"""
    results_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    string_date = list(np.ravel(results_date))[0]
    last_date = dt.datetime.strptime(string_date, "%Y-%m-%d")
    back_year = last_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).filter(Measurement.date >= back_year).all()
    session.close()

    all_temp = []
    for tobs,date in results:
        tobs_dict = ()
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_temp.append(tobs_dict)

    return jsonify(all_temp)


@app.route('/api/v1.0/start')
def calc_temp_start(start):

    session = Session(engine)
    """TMIN, TAVG, AND TMAX list of start dates"""
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.sum(Measurement.tobs)).order_by(Measurement.date >= start).all()

    session.close()

    all_start = []
    for min, max, sum in results:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Max"] = max
        start_dict["Average"] = sum
        all_start.append(start_dict)

    return jsonify(all_start)


@app.route('/api/v1.0/start/end')
def start_and_end(start, end):

    session = Session(engine)
    """TMIN, TAVG, AND TMAX list of start and end dates"""
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.sum(Measurement.tobs)).order_by(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    all_start_end = []
    for min, max, sum in results:
        start_end_dict = {}
        start_end_dict["Min"] = min
        start_end_dict["Max"] = max
        start_end_dict["Average"] = sum
        all_start_end.append(start_end_dict)

    return jsonify(all_start_end)

if __name__ == "__main__":
    app.run(debug=True)



