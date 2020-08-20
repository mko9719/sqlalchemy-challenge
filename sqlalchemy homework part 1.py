#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[19]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from datetime import date, timedelta


# In[5]:


engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()


# In[6]:


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
measure = Base.classes.measurement
stat = Base.classes.station


# In[13]:


#See underlying tables
inspector = inspect(engine)
inspector.get_columns("measurement")


# In[14]:


# Create our session (link) from Python to the DB
session = Session(engine)


# In[17]:


#View Measurement table in Python 
measure_view = session.query(measure.tobs).all()
measure_view


# # Exploratory Climate Analysis

# In[23]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results
dates = session.query(measure.date).all()

# Calculate the date 1 year ago from the last data point in the database
one_year_back = dates[- 1]
one_year_back


# In[28]:


last_date = date(2017,8,23)
prev_year = last_date - timedelta(days=365)


# In[30]:


# Perform a query to retrieve the data and precipitation scores
precipitation = session.query(measure.date, measure.prcp).filter(measure.date>=prev_year).all()
precipitation
# Save the query results as a Pandas DataFrame and set the index to the date column
precip_df = pd.DataFrame(precipitation, columns=['date','prcp'])
precip_df.set_index(precip_df['date'], inplace=True)
precip_df.head()


# In[34]:


# Sort the dataframe by date
precip_df.index.name=None
precip_df.sort_values('date')


# In[38]:


# Use Pandas Plotting with Matplotlib to plot the data
precip_df.plot(rot=90, figsize=(10,5))
plt.xlabel("Date")
plt.ylabel("Inches")
plt.title("Date vs. Inches");


# In[39]:


# Use Pandas to calcualte the summary statistics for the precipitation data
precip_df['prcp'].describe()


# In[42]:


# Design a query to show how many stations are available in this dataset?
stations = session.query(func.count(stat.station)).all()
stations


# In[46]:


# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
active_stations = session.query(measure.station, func.count(measure.station)).group_by(measure.station).order_by(func.count(measure.station).desc()).all()
active_stations


# In[50]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
temp_stats = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).filter(measure.station == "USC00519281").all()
temp_stats


# In[54]:


# Choose the station with the highest number of temperature observations.
highest = session.query(measure.tobs).filter(measure.station == "USC00519281").filter(measure.date>=prev_year).all()
highest[:5]


# In[58]:


# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
highest_df = pd.DataFrame(highest)
highest_df.plot.hist();
plt.xlabel("Temperature")


# ## Bonus Challenge Assignment

# In[ ]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# In[ ]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.


# In[ ]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


# In[ ]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


# In[ ]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")


# In[ ]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# In[ ]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


# In[ ]:


# Plot the daily normals as an area plot with `stacked=False`

