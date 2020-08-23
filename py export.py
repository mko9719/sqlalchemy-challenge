#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# # Reflect Tables into SQLAlchemy ORM

# In[19]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from datetime import date, timedelta
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
measure = Base.classes.measurement
stat = Base.classes.station

#See underlying tables
inspector = inspect(engine)
inspector.get_columns("measurement")

# Create our session (link) from Python to the DB
session = Session(engine)

#View Measurement table in Python 
#measure_view = session.query(measure.tobs).all()
#measure_view


# # Exploratory Climate Analysis
# Design a query to retrieve the last 12 months of precipitation data and plot the results
#dates = session.query(measure.date).all()

# Calculate the date 1 year ago from the last data point in the database
#one_year_back = dates[- 1]
#one_year_back


# In[28]:


#last_date = date(2017,8,23)
#prev_year = last_date - timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
#precipitation = session.query(measure.date, measure.prcp).filter(measure.date>=prev_year).all()
#precipitation

# Save the query results as a Pandas DataFrame and set the index to the date column
#precip_df = pd.DataFrame(precipitation, columns=['date','prcp'])
#precip_df.set_index(precip_df['date'], inplace=True)
#precip_df.head()

# Sort the dataframe by date
#precip_df.index.name=None
#precip_df.sort_values('date')

# Use Pandas Plotting with Matplotlib to plot the data
#precip_df.plot(rot=90, figsize=(10,5))
#plt.xlabel("Date")
#plt.ylabel("Inches")
#plt.title("Date vs. Inches");

# Use Pandas to calcualte the summary statistics for the precipitation data
#precip_df['prcp'].describe()

# Design a query to show how many stations are available in this dataset?
#stations = session.query(func.count(stat.station)).all()
#stations

# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
#active_stations = session.query(measure.station, func.count(measure.station)).group_by(measure.station).order_by(func.count(measure.station).desc()).all()
#active_stations

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
#temp_stats = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).filter(measure.station == "USC00519281").all()
#temp_stats

# Choose the station with the highest number of temperature observations.
#highest = session.query(measure.tobs).filter(measure.station == "USC00519281").filter(measure.date>=prev_year).all()
#highest[:5]

#import pandas as pd
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
#highest_df = pd.DataFrame(highest)
#highest_df.plot.hist();
#plt.xlabel("Temperature")

#Flask Setup
from flask import Flask, jsonify
app = Flask(__name__)

#Route One Set-Up
@app.route("/")
def home():
    return(f"Welcome to our Home page!")
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start<br/>"
    f"/api/v1.0/end<br/>"

#Route Two - Convert Precipiation Query Results to Dictionary
@app.route("/api/v1.0/precipitation") 
def precipitation():
    """Return prior year precipiation data"""

    # Date one year ago from last date...
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Date & precipitation data for prior year...JSONIFY'd 
    precipitation = session.query(measure.date, measure.prcp).\
        filter(measure.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Route Three - List All Stations
@app.route("/api/v1.0/stations")
def stations():
    station_data=session.query(stat.station, stat.name).all()
    stations_list={}
    for result in station_data:
        stations_list[result[0]]=result[1]
    return jsonify(stations_list)

#Route Four - Dates/Temps of Most Active Station in PY
@app.route("/api/v1.0/tobs")
def most_active():
    most_active_station = session.query(measure.station, func.count(measure.station)).group_by(measure.station).order_by(func.count(measure.station)).first()
    most_active_station_data = session.query(measure.station, measure.date, measure.tobs).filter(measure.station == most_active_station)
    dict_list = []
    for x in most_active_station_data:
        dict_list[x[0]]=x[1]
    return jsonify(dict_list)


#Route Five - Start/End Date Statistics


#Debug
if __name__ == '__main__':
    app.run(debug=True)


# %%
