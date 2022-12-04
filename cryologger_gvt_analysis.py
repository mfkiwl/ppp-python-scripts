#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 17:27:49 2022

@author: adam
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pyproj
from pyproj import Proj

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# Add Natural Earth coastline
coast = cfeature.NaturalEarthFeature("physical", "land", "10m",
                                     edgecolor="black",
                                     facecolor="lightgray",
                                     lw=0.5)

# Add Natural Earth coastline
coastline = cfeature.NaturalEarthFeature("physical", "coastline", "10m",
                                         edgecolor="black",
                                         facecolor="none",
                                         lw=0.75)

# Seaborn configuration
sns.set_theme(style="ticks")
sns.set_context("talk") # talk, paper, poster

# Global plot parameters
#plt.rc("legend",fancybox=False, framealpha=1, edgecolor="black")

# Set colour palette
sns.palplot(sns.color_palette("colorblind"))
colours = sns.color_palette("colorblind", 10).as_hex()
sns.set_palette("colorblind", 10)


# -----------------------------------------------------------------------------
# Plotting attributes
# -----------------------------------------------------------------------------

lw = 1
interval = 1
date_format = "%Y-%m-%d"

# Figure DPI
dpi = 300

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

path_data = "/Users/adam/Desktop/gnss/data/merged/"
path_stats = "/Users/adam/Desktop/gnss/data/statistics/"
path_figures = "/Users/adam/Desktop/gnss/figures/"

# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
df = pd.read_csv(path_data + "lowell_upper.csv", index_col=False)
df = pd.read_csv(path_data + "lowell_corner.csv", index_col=False)
df = pd.read_csv(path_data + "belcher_upper.csv", index_col=False)
df = pd.read_csv(path_data + "belcher_lower.csv", index_col=False)


# -----------------------------------------------------------------------------
# Calculate statistics
# -----------------------------------------------------------------------------

# Lowell
df1 = calc_stats(path_data, "lowell_upper")
df2 = calc_stats(path_data, "lowell_corner")

# Belcher
calc_stats(path_data, "belcher_upper")
calc_stats(path_data, "belcher_lower")

def calc_stats(path_data, filename):
    
    # Load concatenated CSV file
    df1 = pd.read_csv(("{}{}.csv".format(path_data, filename)), index_col=False)
    
    # Add date
    df1["date"] = pd.to_datetime(df1["year"] * 1000 + df1["day_of_year"], format="%Y%j")

    # Create empty dataframe
    df2 = pd.DataFrame()
    
    # Group by date and select last row of each day
    df2 = df1.groupby("date").tail(1)
    
    '''
    # Group by date and calculate mean position
    stats = df.groupby("date").agg(latitude_decimal_degree=("latitude_decimal_degree", "mean"),
                                   longitude_decimal_degree=("longitude_decimal_degree", "mean"))
    '''
    # Reset index
    df2 = df2.reset_index()
    
    # Initialize pyproj with appropriate ellipsoid
    geodesic = pyproj.Geod(ellps="WGS84")
        
    # Calculate forward azimuth and great circle distance between modelled coordinates
    df2["direction"], back_azimuth, df2["distance"] = geodesic.inv(df2["longitude_decimal_degree"].shift().tolist(), 
                                                                   df2["latitude_decimal_degree"].shift().tolist(),
                                                                   df2["longitude_decimal_degree"].tolist(), 
                                                                   df2["latitude_decimal_degree"].tolist())
    
    # Convert distance from metres to centimenters
    df2["distance"] = df2["distance"]
    
    # Calculate cumulative distance traveled
    df2["distance_csum"] = df2["distance"].cumsum()
    
    # Convert azimuth from (-180° to 180°) to (0° to 360°)
    df2["direction"] = (df2["direction"] + 360) % 360
    
    # Calculate speed
    df2["speed"] = df2["distance"] / 24
    
    output_file = "{}{}_stats_new.csv".format(path_stats, filename)
    
    # Output file
    df2.to_csv(output_file)

    print("Processed: {}".format(output_file))
    
    return(df2)
    



# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------
df1 = pd.read_csv(path_stats + "milne_2_stats.csv", index_col=False)


# Lowell Glacier
df1 = pd.read_csv(path_stats + "lowell_upper_stats.csv", index_col=False)
df2 = pd.read_csv(path_stats + "lowell_corner_stats_new.csv", index_col=False)

# Find max and min displacements
df1[df1.distance == df1.distance.max()]
df1[df1.distance == df1.distance.min()]

df2[df2.distance == df2.distance.max()]
df2[df2.distance == df2.distance.min()]


# Belcher Glacier
df1 = pd.read_csv(path_stats + "belcher_upper_stats.csv", index_col=False)
df2 = pd.read_csv(path_stats + "belcher_lower_stats.csv", index_col=False)

# Convert datetimes
df1["date"] = pd.to_datetime(df1["date"].astype(str), format="%Y-%m-%d")
df2["date"] = pd.to_datetime(df2["date"].astype(str), format="%Y-%m-%d")

# Convert distance to metres
df1["distance"] = df1["distance"] / 100
df1["distance_csum"] = df1["distance_csum"] / 100

df2["distance"] = df2["distance"] / 100
df2["distance_csum"] = df2["distance_csum"] / 100

# Optional:
    
# Set date as index
df1 = df1.set_index("date")
df2 = df2.set_index("date")

# Find missing dates
pd.date_range(start="2021-07-19", end="2021-12-28").difference(df1.index)
pd.date_range(start="2021-08-31", end="2022-05-27").difference(df2.index)

new= df1 - df2

# -----------------------------------------------------------------------------
# Plots - Speed & Distance
# -----------------------------------------------------------------------------

# Daily displacement
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="date", y="distance", data=df1, color="#0173b2", errorbar=None, label="Milne Glacier 2")
#sns.lineplot(x="date", y="distance", data=df2, color="#de8f05", errorbar=None, label="Lowell Corner")
ax.set(xlabel=None, ylabel="Daily Displacement (m)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "milne_displacement.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Cumulative Distance
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="date", y="distance_csum", data=df1, color="#0173b2", errorbar=None, label="Lowell Upper")
sns.lineplot(x="date", y="distance_csum", data=df2, color="#de8f05", errorbar=None ,label="Lowell Corner")
ax.set(xlabel=None, ylabel="Cumulative Distance (m)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_distance_csum2.png", dpi=dpi, transparent=False, bbox_inches="tight")


# Daily Speed
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="date", y="speed", data=df1, color="#0173b2", errorbar=None, label="Lowell Upper")
sns.lineplot(x="date", y="speed", data=df2, color="#de8f05", errorbar=None ,label="Lowell Corner")
ax.set(xlabel=None, ylabel="Speed (cm h^-1)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_speed.png", dpi=dpi, transparent=False, bbox_inches="tight")



# -----------------------------------------------------------------------------
# Plots - Maps 
# -----------------------------------------------------------------------------

plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.PlateCarree()) 
ax.set_adjustable("datalim")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  color="black", alpha=0.25, linestyle="dotted",
                  x_inline=False, y_inline=False)
gl.rotate_labels = False
gl.top_labels = False
gl.right_labels = False

gl.xpadding=5
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", color="red",
                data=df2, s=50, linewidth=1, edgecolor="black", transform=ccrs.PlateCarree())
#ax.get_legend().remove()

plt.savefig(path_figures + "belcher_upper_day.png", dpi=dpi, transparent=False, bbox_inches="tight")


# Mean
plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.PlateCarree()) 
ax.set_adjustable("datalim")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  color="black", alpha=0.25, linestyle="dotted",
                  x_inline=False, y_inline=False)
gl.rotate_labels = False
gl.top_labels = False
gl.right_labels = False

gl.xpadding=5
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", color="red",
                data=stats, s=50, linewidth=1, edgecolor="black", transform=ccrs.PlateCarree())
#ax.get_legend().remove()

plt.savefig(path_figures + "belcher_upper_raw_mean.png", dpi=dpi, transparent=False, bbox_inches="tight")



# -----------------------------------------------------------------------------
# Static vs Kinematic Comparison
# -----------------------------------------------------------------------------

# Lowell corner high velocity
df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/comparison/20220619_190000_kinematic.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/comparison/20220619_190000_static.csv", index_col=False)

df1 = pd.read_csv("//Users/adam/Desktop/gnss/data/lowell_corner/lowell_corner.csv", index_col=False)

df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/lowell_corner/kinematic/ppp/20210813_190000.csv", index_col=False)


# Lowell upper low velocity
df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/comparison/20211009_190000_upper_kinematic.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/comparison/20211009_190000_upper_static.csv", index_col=False)




df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_new.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats.csv", index_col=False)








# Add date
df1["date"] = pd.to_datetime(df1["year"] * 1000 + df1["day_of_year"], format="%Y%j")
df2["date"] = pd.to_datetime(df2["year"] * 1000 + df2["day_of_year"], format="%Y%j")


# Get final position
lat1 = df1["latitude_decimal_degree"].iloc[-1]
lat2 = df2["latitude_decimal_degree"].iloc[-1]
lon1 = df1["longitude_decimal_degree"].iloc[-1]
lon2 = df2["longitude_decimal_degree"].iloc[-1]

# Calculate distance between final positions
from haversine import haversine_vector, Unit
kinematic = (lat1, lon1) # (lat, lon)
static = (lat2, lon2)
haversine_vector(kinematic, static, Unit.METERS)

# Create dataframe of final positions
d = {"lat": [df1["latitude_decimal_degree"].iloc[-1], df2["latitude_decimal_degree"].iloc[-1]], 
     "lon": [df1["longitude_decimal_degree"].iloc[-1], df2["longitude_decimal_degree"].iloc[-1]]}
df = pd.DataFrame(data=d)

# Initialize pyproj with appropriate ellipsoid
geodesic = pyproj.Geod(ellps="WGS84")
    
# Calculate forward azimuth and great circle distance between modelled coordinates
direction, back_azimuth, df["distance"] = geodesic.inv(df["lon"].shift().tolist(), 
                                                       df["lat"].shift().tolist(),
                                                       df["lon"].tolist(), 
                                                       df["lat"].tolist())
delta = df["distance"].iloc[-1]


import matplotlib as mpl
from matplotlib import cm


# Normalize colourbar
norm = mpl.colors.Normalize(vmin=19, vmax=22)
cmap = cm.get_cmap("Blues")

# Plot static vs. kinematic
fig, ax = plt.subplots(figsize=(10,10))
ax.grid(ls="dotted")
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", c=df1["decimal_hour"], data=df1, s=50, linewidth=0.5, edgecolor="black", norm=norm, cmap=cmap)
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))


scalarmappaple = cm.ScalarMappable(norm=norm, cmap=cmap)
scalarmappaple.set_array(df1["decimal_hour"])
fig.colorbar(scalarmappaple)

df1.columns

ax.get_legend().remove()
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", data=df2, color=colours[3], s=150, linewidth=0.5, edgecolor="black", label="Static")
sns.scatterplot(x="lon", y="lat", data=df, color=colours[8], s=150, linewidth=0.5, edgecolor="black", marker="D", label="Final position")
ax.set_title("Lowell Upper - Δ = {:.2f} m".format(delta), loc="right")
plt.savefig(path_figures + "static_kinematic_upper2.png", dpi=dpi, transparent=False, bbox_inches="tight")


/Users/adam/Desktop/gnss/data/lowell_corner/lowell_corner.csv


plt.figure(figsize=(10,10))



# Plot raw data
plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.PlateCarree()) 
ax.set_adjustable("datalim")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  color="black", alpha=0.25, linestyle="dotted",
                  x_inline=False, y_inline=False)
gl.rotate_labels = False
gl.top_labels = False
gl.right_labels = False

gl.xpadding=5
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", color="red",
                data=df1, s=50, linewidth=1, edgecolor="black", transform=ccrs.PlateCarree())
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", color="blue",
                data=df2, s=50, linewidth=1, edgecolor="black", transform=ccrs.PlateCarree())
#ax.get_legend().remove()

plt.savefig(path_figures + "belcher_upper_day.png", dpi=dpi, transparent=False, bbox_inches="tight")
