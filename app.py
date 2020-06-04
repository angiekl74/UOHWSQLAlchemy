import numpy as numpy
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from collections import defaultdict
import collections

# Database setup
engine = create_engine(("sqlite:///Resources/hawaii.sqlite")) 

# reflect an exiting database into a new model
Base = automap_base()
Base.prepare(engine, reflect = True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Creating Flask routes
 
# Home page
@app.route("/")
def welcome():
        
        return(
            f"Available Routes:<br/>"
            f"<br/>"
            f"Precipitation:  /api/v1.0/precipitation <br/>"
            f"Stations:  /api/v1.0/stations <br/>"
            f"Temperature Observation:  /api/v1.0/tobs <br/>"
            f"Start Date (Enter date using format: yyyy-mm-dd):  /api/v1.0/start_date <br/>"
            f"Start and End Dates (Enter dates using format: yyyy-mm-dd):  /api/v1.0/start_date/end_date <br/>"
            )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
        session = Session(engine)

        results = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date > '2016-08-22').\
                    order_by(Measurement.date).all()
        
        session.close()
        
        # To map keys to lists of items use defaultdict from the collections module 
        # Need to credit Senderle in stackoverflow for code
        # https://stackoverflow.com/questions/11141383/is-there-a-way-to-preserve-duplicate-keys-in-python-dictionary
        
        data = collections.defaultdict(list)
        for k, v in results:
                data[k].append(v)
    
        return jsonify(data)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
        session = Session(engine)
        results = session.query(Station.station, Station.name).all()
        session.close()
        return jsonify(results)

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
        session = Session(engine)

        results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                            filter(Measurement.station == 'USC00519281').\
                            filter(Measurement.date > '2016-08-17').all()
        session.close()

        return jsonify(results)


# /api/v1.0/<start> 
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def startdate(date):

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                                    func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    session.close()  

    return jsonify(results) 

# /api/v1.0/<start>/<end>
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>/<end_date>")
def between_date(start_date, end_date):

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date).all()
  
    session.close()

    return jsonify(results)  


if __name__ == '__main__':
    app.run(debug=True)



