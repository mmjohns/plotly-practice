
# coding: utf-8

# # Plotly: Simple Line and Bar Charts
# ## Practicing and experimenting with Plotly, Python and Data Visualization.
# 
# #### Links:
# - With help from [Plotly User Guide](http://nbviewer.jupyter.org/github/plotly/python-user-guide/tree/master/)
# 
# - Stored in [GitHub](https://github.com/mmjohns/plotly-practice)

# -----

# ### Contents
# 1. [**Setup**](#section1)
# 2. [**Single Line Chart**](#section2)
# 3. [**Dual Line Chart**](#section3)
# 4. [**Grouped Bar Chart with Subplot**](#section4)

# -----

# ## <a id="section1">Set up</a>

# In[60]:

import plotly
import plotly.plotly as py
import plotly.tools as tls 
from plotly.graph_objs import Data, Layout, Figure, XAxis, YAxis, Bar, Marker, Margin, Font, Annotation

import numpy as np


# In[29]:

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


# In[30]:

# Function for the csv file
life_expt_file = '/Users/meganjohns/AnacondaProjects/plotly-practice/data/world_life_expt_by_year.csv'

# Import CSV file and store specific rows as lists
year = get_csv_data(life_expt_file, 'Year')
US_life_expt = get_csv_data(life_expt_file, 'United States')
# Will use later
China_life_expt = get_csv_data(life_expt_file, 'China')


# In[31]:

# Colors
US_color = '#002868'
China_color = '#aa381e'


# ----

# ## <a id="section2">Single Line Chart</a>

# In[32]:

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


# In[33]:

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


# In[34]:

# Call the plot() function of the plotly.plotly submodule,
# save and name figure
# Note: to keep plots private (free accounts have a limit), add argument world_readable=False
# py.plot(fig, filename='simple_US_life_expt_over_time', auto_open=False)

# Embed result in notebook
py.iplot(fig1, filename='simple_US_life_expt_over_time')


# ----

# ## <a id="section3">Dual Line Chart</a>

# In[138]:

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


# In[139]:

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
        range=[0, 80]
    ),
    font=dict(family='Droid Serif', size=16)
)

# Make Figure object
fig2 = Figure(data=trace2, layout=layout2)


# In[140]:

# (@) Send to Plotly and show in notebook
py.iplot(fig2, filename='simple_US_Ch_life_expt_over_time')


# ----

# ## <a id="section4">Grouped Bar Chart with Subplot</a>

# Import GDP csv file

# In[7]:

# Function for the csv file
gdp_file = '/Users/meganjohns/AnacondaProjects/plotly-practice/data/world_gdp_by_year.csv'

# Import CSV file and store specific rows as lists
US_gdp = get_csv_data(gdp_file, 'United States')
China_gdp = get_csv_data(gdp_file, 'China')


# Make subplots - will share x-axis

# In[75]:

# Generate Figure object with 2 axes on 2 rows, print axis grid to stdout
fig = tls.make_subplots(
    rows=2, 
    cols=1,
    shared_xaxes=True
)


# In[76]:

# Define a trace-generating function (returns a Bar object)
def make_trace(y, color, name, sbplt):
    return Bar(
        x=year,
        y=y,            # take in the y-coords     
        name=name,      # label for hover
        marker=Marker(color=color),  # set bar color
        xaxis='x1',                    # (!) both subplots on same x-axis
        yaxis='y{}'.format(sbplt)      # (!) plot on y-axis of 'sbplt'
    )


# Build the data object

# In[77]:

# Assign gdp traces to 'xaxis2' and 'yaxis2' (top axis)
traces_T = [make_trace(US_gdp, US_color, 'United States', 2),
            make_trace(China_gdp, China_color, 'China', 2)]

# Assign life_expt traces to 'xaxis' and 'yaxis' (bottom axis)
traces_B = [make_trace(US_life_expt, US_color, 'United States', 1),
            make_trace(China_life_expt, China_color, 'China', 1)]

# Concatenate the four traces and set the 'data' key in the Figure object
fig['data'] = Data(traces_T + traces_B)


# In[130]:

# Make Layout object
layout = Layout(
    barmode='group',  # (!) bars are in groups on this plot
    bargroupgap=0,    # norm. spacing between group members
    bargap=0.25,       # (!) spacing (norm. w.r.t axis) between bars
    title="<b>U.S. and China GDP and Life Expectancy Over Time</b><br>\
    (1952-2007)",    
    showlegend=False, # remove legend
    plot_bgcolor='#EFECEA',  # set plot and 
    paper_bgcolor='#EFECEA', #   frame background color
    autosize=False,   # (!) turn off autosize 
    height=500,
    width=750,
    margin=Margin( # set frame to plotting area margins
        t=100,     #   top,
        b=100,     #   bottom,
        r=25,      #   right,
        l=70       #   left
    ), 
    font=Font(
        family="Droid Sans, sans-serif", 
        color='#635F5D'
    ),
    xaxis= XAxis(
        gridcolor='white',  # white grid lines
        gridwidth=2,        # bigger grid lines
        zeroline=False,     # remove thick zero line
        ticks='outside',    # draw ticks outside axes
        autotick=False,     # (!) overwrite default tick options
        dtick=100,          # (!) set distance between ticks  
        ticklen=8,          # (!) set tick length
        tickwidth=1.5       #     and width
    )
)     


# In[131]:

# Define a function for updating up the axes (return a dictionary)
def update_axis(title, tickangle):
     return dict(
        title=title,              # axis title
        tickfont=dict(size=13),   # font size, default is 12
        tickangle=tickangle,      # set tick label angles
        gridcolor='#FFFFFF',      # white grid lines
        zeroline=False            # remove thick zero line
    )
             
# Update top axis options in the 'layout' key in Figure object
fig['layout']['xaxis1'].update(
    update_axis('', 0)
)

# Update top axis options in Layout options
fig['layout']['yaxis2'].update(
    update_axis('<b>GDP</b>', 0)
) 

# Update bottom axis options in Layout object
fig['layout']['yaxis1'].update(
    update_axis('<b>Life Expectancy</b>', 0)
)

fig['layout'].update(
    showlegend=False, # remove legend
    autosize=False,   # (!) turn off autosize
    plot_bgcolor='#EFECEA',  # set plot and 
    paper_bgcolor='#EFECEA', #   frame background color
)   


# Add Title

# In[132]:

# Define a 1st annotation-generating function (for title and data source)
def make_anno1(text, fontsize, x, y):
    return Annotation(
        text=text,   # annotation text
        xref='paper',  # use paper coordinates
        yref='paper',  #   for both x and y coords
        x=x,           # x and y position 
        y=y,           #   in norm. coord. 
        font=Font(size=fontsize),  # text font size
        showarrow=False,       # no arrow (default is True)
        bgcolor='#F5F3F2',     # light grey background color
        bordercolor='#FFFFFF', # white borders
        borderwidth=1,         # border width
        borderpad=10     # set border/text space to 1 fontsize
    )

# (2.5a) Create annotation list with title and data source
annotations = [
    make_anno1('<b>U.S. and China<br>GDP and Life Expectancy Over Time</b>', 16, 0, 1.26)
]


# Add Legend

# In[133]:

# Define annotation-generating function (for the legend)
def make_anno2(text, fontcolor, x):
    return Annotation(
        text=text,  # annotation text
        xref='paper',     # use paper coordinates
        yref='paper',     #   for both x and y coords
        x=x,              # x and y position
        y=1.2,            #   in norm. coord.
        xanchor='right',  # 'x' at right border of annotation
        font=Font(
            size=12,           # set text font size 
            color=fontcolor    #   and color
        ),
        showarrow=False,   # no arrow (default is True)
        bgcolor='#F5F3F2', # light grey background color
        borderpad=10       # set border/text space (in pixels)
    )

# (2.5b) Append annotation list with the two legend items
annotations += [
    make_anno2('<b>United States</b>', US_color, 0.9),
    make_anno2('<b>China</b>', China_color, 1)
]

# (2.5c) Add annotation list to 'layout' key in the Figure object
fig['layout'].update(
    annotations=annotations
)


# Call to Plotly

# In[134]:

# Send to Plotly and show in notebook
py.iplot(fig, filename='subplot_US_China_gdp_life_expt_over_time')

