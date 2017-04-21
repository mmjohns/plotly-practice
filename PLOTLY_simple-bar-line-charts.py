
# coding: utf-8

# # Plotly: Simple Line Charts
# ## Practicing and experimenting with Plotly, Python and Data Visualization.
# 
# #### Links:
# - With help from [Plotly User Guide](http://nbviewer.jupyter.org/github/plotly/python-user-guide/tree/master/)
# 
# - Stored in [GitHub](https://github.com/mmjohns/plotly-practice/blob/master/PLOTLY_simple-bar-line-charts.ipynb)

# -----

# ### Contents
# 1. [**Setup**](#section1)
# 2. [**Single Line Chart**](#section2)
# 3. [**Dual Line Chart**](#section3)

# -----

# ## <a id="section1">Set up</a>

# In[10]:

import plotly
import plotly.plotly as py
import plotly.tools as tls 
from plotly.graph_objs import Data, Layout, Figure, XAxis, YAxis

import numpy as np


# In[6]:

# (*) csv file read/write
import csv         

# Define a csv reader function
def get_csv_data(filepath, row_id):
    ''' 
    Read row of csv file, return a numpy array where
    each entry corresp. to a particular year
    pos. arg (1) filepath: relative path to csv file 
    pos. arg (2) row_id: id of row requested, found in first column (a string)
    '''
    with open(filepath, 'r') as data_file:
        reader = csv.reader(data_file)        # define reader object
        for row in reader:                    # loop through rows in csv file
            if len(row) and row_id in row[0]: # test for empty lines and row id
                # Trim 1st entry
                # and return a numpy array
                return np.array([float(x) for x in row[1:]])
            
# The 'with' statement automatically closes 'filepath' at the end of its block of code


# In[7]:

# Function for the csv file
life_expt_file = '/Users/meganjohns/AnacondaProjects/plotly-practice/data/world_life_expt_by_year.csv'

# Import CSV file and store specific rows as lists
year = get_csv_data(life_expt_file, 'Year')
US_life_expt = get_csv_data(life_expt_file, 'United States')
# Will use later
China_life_expt = get_csv_data(life_expt_file, 'China')


# In[8]:

# Colors
US_color = '#002868'
China_color = '#aa381e'


# ----

# ## <a id="section2">Single Line Chart</a>

# In[9]:

# Make a dictionary linking x and y coordinate lists to 'x' and 'y' keys
trace1 = dict(
    x=year, 
    y=US_life_expt,
    line = dict(
        color = US_color,
        width = 4
    ),
    marker=dict(size = 12)
)

# Make list of trace, to be sent to Plotly
data1 = [trace1]


# In[19]:

# Make Layout object
layout1 = Layout(
    title="<b>U.S. Life Expectancy Over Time</b><br>\
    (1952-2007)",
    showlegend=False,
    yaxis= YAxis(
        title='Life Expectancy (years)',
        showgrid=False
    ),
    xaxis= XAxis(
        title='Year',
        showgrid=False
    )
)

# Make Figure object
fig1 = Figure(data=data1, layout=layout1)


# In[20]:

# Call the plot() function of the plotly.plotly submodule,
# save and name figure
# Note: to keep plots private (free accounts have a limit), add argument world_readable=False
# py.plot(fig, filename='simple_US_life_expt_over_time', auto_open=False)

# Embed result in notebook
py.iplot(fig1, filename='simple_US_life_expt_over_time')


# ----

# ## <a id="section3">Dual Line Chart</a>

# In[34]:

# Define a trace-generating function (returns a Line object)
def make_trace(y, color, name):
    return dict(
        x = year,
        y = y,
        name = name,
        line = dict(
            color = color,
            width = 4
        ),
        marker=dict(size = 12)
    )


# In[60]:

# Build the data object
# Assign temp traces to top axis
trace2 = [make_trace(US_life_expt, US_color, 'US'),
           make_trace(China_life_expt, China_color, 'China')]


# Make Layout object
layout2 = Layout(
    title="<b>U.S. and China Life Expectancy Over Time</b><br>\
    (1952-2007)",
    yaxis= YAxis(
        title='Life Expectancy (years)',
        showgrid=False,
    ),
    xaxis= XAxis(
        title='Year',
        showgrid=False,
    ),
    font=dict(family='Droid Serif', size=16)
)

# Make Figure object
fig2 = Figure(data=trace2, layout=layout2)


# In[61]:

# (@) Send to Plotly and show in notebook
py.iplot(fig2, filename='simple_US_Ch_life_expt_over_time')

