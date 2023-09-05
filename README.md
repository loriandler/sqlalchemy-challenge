# sqlalchemy-challenge
Module 10 Challenge for UM Bootcamp

# Background
Congratulations!  You've decided to treat yourself to a lovely holiday vacation in Honolulu, Hawaii.  To help with the trip planning, you decide to do a climate analysis about the area. 

# Overview
The work with this assignment came together with Jupyter Notebook, data visualization, data manipulation, and database operations using Python libraries like Matplotlib, NumPy, Pandas, SQLAlchemy, and SQLite.

There were two parts to the assignment.

## Part 1: Analyze and Explore the Climate Data
SQLAlchemy ORM Queries, Pandas, and Matplotlib were used to connect to an SQLite database, reflect tables into classes and link by creating an SQLAlchemy session.  Then Precipitation Analysis and a station analysis was done.

SQLAlchemy functions of create_engine() and automap_base() were used to explore the climate data.

### Precipitation Analysis
Precipitation analysis involved finding the most recent date in the data set, getting th previous 12 months of precipitation data, selecting only the "date" and "prcp" values, loading results into a Pandas DataFrame and sorting the values by date.  The results were plotted in a bar chart.  Summary statistics were printed for the precipitation data.

### Station Analysis
Stations were counted and the most-active stations were displayed in descending order with a list.  The lowest, highes, and average temperatures were found for the most-active station.  The 12 months of temperature observations (tobs) data was plotted in a histogram.

## Part 2: Design Your Climate App
Created for this was a homepage with available routes, precipitation results, a list of stations, temperature observations, and analysis from a particular start date or for a particular set of dates was provided.

# Credits
Thank you to the tutor, Kyle Goode, who helped with some typographical errors and some file paths with me.

Thank you to Hunter Hollis, instructor, and TA's Rand & Sam for all of their teaching and support during this week's lessons of the Bootcamp.


