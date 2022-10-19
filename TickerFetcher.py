#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from bokeh.palettes import Spectral5
from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc


# 

# Purpose: Output an interactive HTML plot for the normalized adjusted close data of given Ticker names and date frame.
# 
# Metrics: "Performance" refers to normalized adjusted closing prices over a given timeframe.
# 
# Data Source: Yahoo Finance
# 
# Requisites: None, just input Ticker symbols and start/end dates in YYYY-MM-DD format.
# 
# Alternative Uses: I also have a little snippet of code, the Retrieve function, that retrieves and downloads MAX historical data for given Ticker symbols as an unedited CSV file named "TickerSymbol.csv".

# 

# In[2]:


def Retrieve():
    '''Retrieves max Historical Data for input tickers and downloads the CSV file unedited'''
    Tickers = []
    Tickers = [item for item in input("Enter the Tickers you wish to retrieve: ").split()]
    for i in Tickers:
        Historical = yf.Ticker(i)
        df = pd.DataFrame(Historical.history(period="max"))
        df.reset_index(inplace = True)
        print(i)
        print(df)
        df.to_csv('{}.csv'.format(i), header = True, index = False, encoding = 'utf-8')


# 

# In[3]:


def adjClose_Grouped():
    '''Returns ONLY Adjusted Closing Historical values for input tickers and Groups them into a single table'''
    Tickers = []
    Tickers = [item for item in input("Enter the Tickers you wish to retrieve: ").split()]
    SD = input("Enter the Start Date YYYY-MM-DD: ")
    ED = input("Enter the End Date YYYY-MM-DD: ")
    data = yf.download(Tickers, start = SD, end = ED)
    data = data[["Adj Close"]]
    return(data)


# 

# In[5]:


def normalize_data(df):
    '''Normalizes datasets by dividing all values by the first'''
    return df/df.iloc[0, :]


# 

# In[6]:


def norm_Grouped_Data():
    '''
    Utilizes adjClose_Grouped function to retrieve grouped adj closed data, then normalizes that data with the 
    normalize_data function
    '''
    data = adjClose_Grouped()
    data_n = normalize_data(data)
    return(data_n)
    type(data_n)


# 

# In[19]:


def plot_data():
    '''Plots Grouped Normalized Stock Adjusted Close data from yahoo finance.'''
    data2 = norm_Grouped_Data()
    data = data2.dropna(axis='columns', how ='all')
    
    data.columns = ['{}'.format(x[1]) for x in data.columns]

    curdoc().theme = 'dark_minimal'
    p = figure(width=1500, height=500, x_axis_type="datetime")
    p.title.text = 'Click on legend entries to hide the corresponding lines'
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Normalized Performance'
    df = pd.DataFrame(data) 
    for x, color in zip(df.columns, Spectral5):
        p.line(df.index, df[x], line_width=2, alpha=0.8, color = color, muted_color = color, legend_label= str('{}'.format(x)))

    p.legend.location = "top_left"
    p.legend.click_policy="mute"

    output_file("TopFive.html", title="Top Five Performers")

    show(p)    


# In[20]:


plot_data()

