import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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

@app.route("/api/v1.0/precipitation")
def last_12_mth_prcp():
    # Calculate the date 2 year ago from today
    last_to_last_yr = dt.date.today() - dt.timedelta(days=2*365)

    # Perform a query to retrieve the data and precipitation scores
    result = session.query(Measurement.date, func.sum(Measurement.prcp).label("prcp")).filter(Measurement.date>last_to_last_yr).\
                group_by(Measurement.date).order_by(Measurement.date).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_station_prcp = []
    
    for row in result:
        row_dict = {}
        row_dict["date"] = row.date
        row_dict["precipitation"] = row.prcp
        all_station_prcp.append(row_dict)

    return jsonify(all_station_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    st_results = station_count = session.query((func.distinct(Measurement.station).label("station"))).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_names = list(np.ravel(st_results))

    return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
