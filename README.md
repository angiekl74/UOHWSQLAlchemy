## SQLAlchemy Challenge - Surfs Up!

## Table of contents
* [Homework_Assignment_Background](##Homework_Assignment_Background)
* [Project_Task](##Project_Task)
* [Technologies](##Technologies)
* [Setup](##setup)
* [Methodology](##Methodology)


## Homework_Assignment_Background 

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.


## Project_Task 

1. Completed a precipitation analysis
    * Designed a query to retrieve the last 12 months of precipitation data.
    * Selected only the date and precipitation values.
    * Loaded the query results into a Pandas DataFrame and set the index to the date column.
    * Sorted the DataFrame values by date.
    * Plotted the results using the DataFrame plot method.
    * Used Pandas to print the summary statistics for the precipitation data.

2. Completed a station analysis
    * Designed a query to calculate the total number of stations.
    * Designed a query to find the most active stations.
    * Listed the stations and observation counts in descending order.
    * Determined which station has the highest number of observations.
    * Designed a query to retrieve the last 12 months of temperature observation data (TOBS).
    * Filtered by the station with the highest number of observations.
    * Plotted the results as a histogram with bins=12.

3. Designed a Flask API to display the above analysis
    * Created the following 5 routes:
        * /
            * Home page
            * Lists all routes that are available
        * /api/v1.0/precipitation
            * Converted the query results to a dictionary using date as the key and precipitation as the value.
            * Returned the JSON representation of your dictionary.
        * /api/v1.0/stations
            * Returned a JSON list of stations from the dataset.
        * /api/v1.0/tobs
            * Queried the dates and temperature observations of the most active station for the last year of data.
            * Returned a JSON list of temperature observations (TOBS) for the previous year.
        * /api/v1.0/<start> and /api/v1.0/<start>/<end>
            * Returned a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
            * When given the start only, it will calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
            * When given the start and the end date, it will calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


## Technologies
The project is created with:

* jupyter==1.0.0
* pandas==0.25.1
* sqlalchemy===1.3.16
* numpy===1.18.3
* flask==1.1.1
* matplotlib===3.2.1


## Setup
1. To install jupyter botebook (https://jupyter.org/install) 
2. To install splinter (https://pypi.org/project/splinter/)
3. To install pandas (https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
4. To install sqlAlchemy (https://pypi.org/project/SQLAlchemy/)
5. To install matplotlib (https://matplotlib.org/3.2.1/users/installing.html)
6. To install numpy (https://pypi.org/project/numpy/)


## Methodology

1. Wrote code to find data required in project task (To review code and charts created using matplotlib: climate_starter.ipynb).  

2. Created flask app with the following routes specified by project task (To review code: app.py).  Examples of the code is shown below: 
    * Created a home route
    ```python
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
    ```

    * Created route to filter by start and end date
    ```python
    @app.route("/api/v1.0/<start_date>/<end_date>")
    def between_date(start_date, end_date):

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date).all()
  
    session.close()
    return jsonify(results)  
    ```

4. To visualize flask app in action, you must run the app.py file from the terminal. 

    * Open terminal and type:
        ```python
        python app.py
        ```
    * In address bar, to view the home page, type:
        ```
        http://localhost:5000/
        ```                                   
    * Select the route you wish to filter the data by.  Example:
        ```
        http://localhost:5000/api/v1.0/tobs
        ```
    * Below are snapshots of the home route and returned json formatted filtered data for the 
    http://localhost:5000/api/v1.0/tobs route:

    <img src="Images/final_hw1.png" width="500" height="400">

    <img src="Images/final_hw2.png" width="300" height="700">


