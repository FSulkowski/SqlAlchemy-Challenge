# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

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
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
  
    most_recent_date_str = session.query(func.max(Measurement.date)).scalar()


    most_recent_date = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d")
    
    
    one_year_ago = most_recent_date - dt.timedelta(days=366)

   
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    
    precipitation_dict = {date: prcp for date, prcp in precip_data}

    return jsonify(precipitation_dict)



@app.route("/api/v1.0/stations")
def stations():
   
    results = session.query(Station.station).all()

 
    all_stations = list(np.ravel(results))


    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    
    most_active_station = 'USC00519281'
    

    
    most_recent_date_str = session.query(func.max(Measurement.date)).scalar()
    
    most_recent_date = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d")
    
    
    one_year_ago = most_recent_date - dt.timedelta(days=366)

    
    tobs_data = session.query(Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year_ago).all()

    
    temps = list(np.ravel(tobs_data))

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
  
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
      
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

  
    temps = list(np.ravel(results))

    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)