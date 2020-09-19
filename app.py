
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import numpy as np
# create engine
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
# step 1:
app = Flask(__name__)
@app.route("/")
def helloWorld():
    # urls that tell the user the end points that are available
    return "Hello World"
@app.route("/stations")
def stations():
    # return a list of all the stations in JSON Format
    listOfStations = session.query(Station.station).all()
    stationOneDimension = list(np.ravel(listOfStations))
    return jsonify(stationOneDimension)
#2nd step:
if __name__ == '__main__':
    app.run()
