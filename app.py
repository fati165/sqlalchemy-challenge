from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from sqlalchemy import Column, Integer, String, Float, Date, desc

import numpy as np
import datetime as dt
# create engine
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
print (Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
# step 1:
app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/stations")
def stations():
    # return a list of all the stations in JSON Format
    listOfStations = session.query(Station.station).all()
    stationOneDimension = list(np.ravel(listOfStations))
    return jsonify(stationOneDimension)

@app.route("/api/v1.0/precipitation")
def precipt():
#Convert the query results to a dictionary using date as the key and prcp as the value.
#eturn the JSON representation of your dictionary.
    lastday = dt.date(2017,8,23)
    lastminus1= lastday- dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation scores
    lastyear= session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= lastminus1).all()
    precipitation= {}
#append dict
    for date, precipt in lastyear:
        precipitation[date]= precipt
    return jsonify(precipitation)
@app.route("/api/v1.0/tobs")
def tobs():
    lastday = dt.date(2017,8,23)
    lastminus1= lastday- dt.timedelta(days=365)
    tempobserve = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= lastminus1).\
    group_by(Measurement.date).all()
    temp = list(np.ravel(tempobserve))
    return jsonify(temp)

@app.route("/api/v1.0/<start>") 
def starter(start):
# Return a JSON list of the minimum temperature, the average temperature, 
    tobs_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    
    return jsonify(tobs_data)

# When given the start and the end date, calculate the TMIN, TAVG,
#  and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    tobs_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(and_(Measurement.date >= start, Measurement.date <= end)).all()
    
    return jsonify(tobs_data)


#2nd step:
if __name__ == '__main__':
    app.run()