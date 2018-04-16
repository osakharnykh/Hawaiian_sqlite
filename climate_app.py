import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.Measurement
Station=Base.classes.Station

session = Session(engine)

# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    #assignment specifically asks for tobs!
    start_date=dt.datetime.now()-dt.timedelta(days=365)
    start_date=start_date.strftime("%Y-%m-%d")

    tobs_12m=session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date > start_date).\
        order_by(Measurement.date).all()
    
    return jsonify(tobs_12m)
  
@app.route("/api/v1.0/stations")
def stat():

    stations=session.query(Measurement.station).distinct()
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
#very ambiguous description - 'previous year'
def tobs():

    tobs_2017=session.query(Measurement.tobs).\
                filter(Measurement.date > '2017-01-01').\
                filter(Measurement.date < '2017-12-31')
    
    return jsonify(tobs_2017)

@app.route("/api/v1.0/<start>")
def start_only(start):
    tmin=session.query(func.min(Measurement.tobs)).\
                filter(Measurement.date > start)
    tavg=session.query(func.avg(Measurement.tobs)).\
                filter(Measurement.date > start)
    tmax=session.query(func.max(Measurement.tobs)).\
                filter(Measurement.date > start)
    return jsonify([tmin.first()[0],tavg.first()[0],tmax.first()[0]])

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    tmin=session.query(func.min(Measurement.tobs)).\
                filter(Measurement.date > start).\
                filter(Measurement.date < end)
    tavg=session.query(func.avg(Measurement.tobs)).\
                filter(Measurement.date > start).\
                filter(Measurement.date < end)
    tmax=session.query(func.max(Measurement.tobs)).\
                filter(Measurement.date > start).\
                filter(Measurement.date < end)
    return jsonify([tmin.first()[0],tavg.first()[0],tmax.first()[0]])

if __name__ == '__main__':
    app.run(debug=True)

