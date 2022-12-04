#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 9 10:28:41 2022

@author: Adam Garbo

Code to:
    

"""

import glob
import zipfile
import shutil
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pyproj

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------




# -----------------------------------------------------------------------------
# Plotting attributes
# -----------------------------------------------------------------------------

# Seaborn configuration
sns.set_theme(style="ticks")
sns.set_context("talk") # talk, paper, poster

# Set color palette
sns.set_palette("colorblind", 10)

lw = 1
interval = 1
date_format = "%Y-%m"

# Figure DPI
dpi = 300


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

# Set function inputs
path_data = "/Users/adam/Desktop/gnss/data/"
path_figures = "/Users/adam/Desktop/gnss/figures/"

# -----------------------------------------------------------------------------
# Datasets
# -----------------------------------------------------------------------------

# Belcher
filename = "belcher_lower"
filename = "belcher_upper"

# Lowell
filename = "lowell_upper"
filename = "lowell_corner"

# Milne
filename = "milne_1"
filename = "milne_2"

# -----------------------------------------------------------------------------
# Execute functions
# -----------------------------------------------------------------------------

# Process data
process_ppp(path_data,filename)

# Check data
check_data(path_data, filename)

# Calculate statistics
calculate_stats(path_data, filename)

# Produce plots
plot_graphs(path_data,path_figures,"lowell_upper","lowell_corner")

# -----------------------------------------------------------------------------
# Function: Unzip and concatenate CSRS-PPP outputs
# -----------------------------------------------------------------------------
def process_ppp(path_data, filename):
    
    path_input = "{}{}/".format(path_data,filename)
    path_output = "{}ppp/".format(path_input)
    
    # Create output path if required 
    try:
        Path(path_output).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("{} already exists".format(path_output))
    else:
        print("{} folder was created".format(path_output))
    
    # Unzip files
    files = sorted(glob.glob(path_input + "*.zip"))
    for file in files: 
        with zipfile.ZipFile(file) as item: # Treat the file as a zip
            item.extractall(path_output)  # Extract it in the working directory
       
    # Concatenate CSV files
    files = sorted(glob.glob(path_output + "*.csv"))
    with open(path_input + filename + ".csv", "w") as outfile:
        for i, file in enumerate(files):
            with open(file, 'r') as infile:
                if i != 0:
                    infile.readline()  # Throw away header on all but first file
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(infile, outfile)
                print("{} has been imported.".format(file))

# -----------------------------------------------------------------------------
# Function: Perform quality control of concatenated CSV
# -----------------------------------------------------------------------------
def check_data(path_data, filename):

    # Load concatenated CSV file
    df = pd.read_csv("{}{}/{}.csv".format(path_data,filename,filename), index_col=False)
    
    # Add date column
    df["date"] = pd.to_datetime(df["year"] * 1000 + df["day_of_year"], format="%Y%j")
    
    # Set data date range
    data_start = df.date.min()
    data_end = df.date.max()
    
    # Set date as index
    df = df.set_index("date")
    
    # Find missing dates
    data_gaps = pd.date_range(start=data_start, end=data_end).difference(df.index).format(formatter=lambda x: x.strftime("%Y-%m-%d"))
    return(data_gaps)

# -----------------------------------------------------------------------------
# Function: Calculate statistics
# -----------------------------------------------------------------------------

def calculate_stats(path_data, filename):

    path_output = "{}statistics/".format(path_data)
    
    # Create output path if required 
    try:
        Path(path_output).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("{} already exists".format(path_output))
    else:
        print("{} folder was created".format(path_output))

    # Load concatenated CSV file
    df1 = pd.read_csv("{}{}/{}.csv".format(path_data,filename,filename), index_col=False)
    
    # Add date column
    df1["date"] = pd.to_datetime(df1["year"] * 1000 + df1["day_of_year"], format="%Y%j")
    
    # Create empty data frame
    df2 = pd.DataFrame() 
    
    # Group by date and select last row of each day
    df2 = df1.groupby("date").tail(1)
    """
    # Aggregate data by day
    df2 = df1.groupby("date").agg(latitude_decimal_degree=("latitude_decimal_degree", "mean"),
                                  longitude_decimal_degree=("longitude_decimal_degree", "mean"))
    """
    # Reset dataframe index
    df2 = df2.reset_index()
    
    # Initialize pyproj with appropriate ellipsoid
    geodesic = pyproj.Geod(ellps="WGS84")
        
    # Calculate forward azimuth and great circle distance between modelled coordinates
    df2["direction"], back_azimuth, df2["distance"] = geodesic.inv(df2["longitude_decimal_degree"].shift().tolist(), 
                                                                   df2["latitude_decimal_degree"].shift().tolist(),
                                                                   df2["longitude_decimal_degree"].tolist(), 
                                                                   df2["latitude_decimal_degree"].tolist())
    
    # Convert distance from metres to centimenters
    df2["distance"] = df2["distance"] * 100.0
    
    # Calculate cumulative distance traveled
    df2["distance_csum"] = df2["distance"].cumsum()
    
    # Convert azimuth from (-180° to 180°) to (0° to 360°)
    df2["direction"] = (df2["direction"] + 360) % 360
    
    # Calculate speed
    df2["speed"] = df2["distance"] / 24
    
    #df2["distance"] = df2["distance"] / 100000.0
    
    # Export to CSV
    df2.to_csv("{}{}_stats.csv".format(path_output,filename))

# -----------------------------------------------------------------------------
# Function: Plot speed & distance
# -----------------------------------------------------------------------------

def plot_graphs(path_data,path_figures,filename1,filename2):

    # Create output path if required 
    try:
        Path(path_figures).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("{} already exists".format(path_figures))
    else:
        print("{} folder was created".format(path_figures))
        
    # Load data
    df1 = pd.read_csv("{}statistics/{}_stats.csv".format(path_data,filename1), index_col=False)
    df2 = pd.read_csv("{}statistics/{}_stats.csv".format(path_data,filename2), index_col=False)
    
    # Convert datetimes
    df1["date"] = pd.to_datetime(df1["date"].astype(str), format="%Y-%m-%d")
    df2["date"] = pd.to_datetime(df2["date"].astype(str), format="%Y-%m-%d")
    df1["distance"] = df1["distance"] / 100.0
    df2["distance"] = df2["distance"] / 100.0
    df1["distance_csum"] = df1["distance_csum"] / 100.0
    df2["distance_csum"] = df2["distance_csum"] / 100.0

    # Daily displacement
    fig, ax = plt.subplots(figsize=(10,5))
    ax.grid(ls="dotted")
    sns.lineplot(x="date", y="distance", data=df1, errorbar=None, label="Belcher Upper")
    sns.lineplot(x="date", y="distance", data=df2, errorbar=None, label="Belcher Lower")
    ax.set(xlabel=None, ylabel="Daily Displacement (m)")
    plt.xticks(rotation=45, horizontalalignment="right")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    sns.despine()
    ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
    plt.savefig("{}{}_speed.png".format(path_figures,filename1), dpi=dpi, transparent=False, bbox_inches="tight")
    
    # Cumulative Distance
    fig, ax = plt.subplots(figsize=(10,5))
    ax.grid(ls="dotted")
    sns.lineplot(x="date", y="distance_csum", data=df1, errorbar=None, label="Belcher Upper")
    sns.lineplot(x="date", y="distance_csum", data=df2, errorbar=None, label="Belcher Lower")
    ax.set(xlabel=None, ylabel="Cumulative Distance (m)")
    plt.xticks(rotation=45, horizontalalignment="right")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    sns.despine()
    ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
    plt.savefig("{}{}_distance.png".format(path_figures,filename1), dpi=dpi, transparent=False, bbox_inches="tight")


















