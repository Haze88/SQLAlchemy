import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#Flask Setup
app = Flask(__name__)
#Last year of most recent date in dataset
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

@app.route("/")
def home():
    return(
        f"Welcome to the Cool Page <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/(start) <br/>"
        f"/api/v1.0/(start)/(end)"
    )


@app.route("/api/v1.0/precipitation")
def climate_precip():
     # Create our session (link) from Python to the DB
    session = Session(engine)
    sel = [Measurement.date, Measurement.prcp]
    year_prcp = session.query(*sel).filter(Measurement.date>=year_ago,Measurement.prcp!= None).\
    order_by(Measurement.date).all()
    res={date:prcp for date, prcp in year_prcp}
    session.close()
    return jsonify (res)
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations= list(np.ravel(session.query(Station.station).all()))
    session.close()
    return jsonify(stations)
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    year_temp=session.query(Measurement.tobs).filter(Measurement.date>=year_ago,Measurement.station=='USC00519281').\
    order_by(Measurement.tobs).all()
    resp=list(np.ravel(year_temp))
    session.close()
    return jsonify(resp)
@app.route("/api/v1.0/<start>")
def start_fn(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    x=dt.datetime.strptime(start,"%m-%d-%Y")
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=x).all()
    resp=list(np.ravel(results))
    session.close()
    return jsonify(resp)
@app.route("/api/v1.0/<start>/<end>")
def startend_fn(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    x=dt.datetime.strptime(start,"%m-%d-%Y")
    y=dt.datetime.strptime(end,"%m-%d-%Y")
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date>=x).filter(Measurement.date<=y).all()
    print (results)
    resp=list(np.ravel(results))
    session.close()
    return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True)







