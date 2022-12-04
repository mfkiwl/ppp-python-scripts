#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 11:28:31 2022

@author: adam
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import pyproj


# -----------------------------------------------------------------------------
# Plot concatenated output data
# -----------------------------------------------------------------------------

# Load data
df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/lowell_corner/lowell_corner_kinematic.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/lowell_corner/lowell_corner_static.csv", index_col=False)

# Add date column
df1["date"] = pd.to_datetime(df1["year"] * 1000 + df1["day_of_year"], format="%Y%j")
df2["date"] = pd.to_datetime(df2["year"] * 1000 + df2["day_of_year"], format="%Y%j")


start = "2022-05-31"
stop = "2022-06-08"

# Subset by date
df1 = df1[(df1["date"] > start) & (df1["date"] < stop)]
df2 = df2[(df2["date"] > start) & (df2["date"] < stop)]



# Plot all (or a subset) data
fig, ax = plt.subplots(figsize=(10,10))
ax.grid(ls="dotted")
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", data=df1, 
                s=200, linewidth=0.5, edgecolor="black")
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", data=df1, label="Kinematic",
                s=150, linewidth=0.5, edgecolor="black")
#ax.get_legend().remove()
plt.savefig(path_figures + "test.png", dpi=dpi, transparent=False, bbox_inches="tight")




# Plot all (or a subset) data
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="date", y="delta", data=df3, s=50, label="Lowell Upper")
sns.scatterplot(x="date", y="delta", data=df4, s=50, label="Lowell Corner")
ax.set(xlabel=None, ylabel="Static Mean - Final Delta (cm)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_static_mean_final_delta.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Plot map
plt.figure(figsize=(10,5))
ax = plt.axes(projection=ccrs.PlateCarree()) 
ax.set_adjustable("datalim")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  color="black", alpha=0.25, linestyle="dotted",
                  x_inline=False, y_inline=False)
gl.rotate_labels = False
gl.top_labels = False
gl.right_labels = False
gl.xpadding=5
sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", data=df1, label="Lowell Corner",
                s=150, linewidth=0.5, edgecolor="black")

plt.savefig(path_figures + "lowell_corner_scatter.png", dpi=dpi, transparent=False, bbox_inches="tight")


sns.scatterplot(x="longitude_decimal_degree", y="latitude_decimal_degree", data=df1, label="Static",
                color=colours[1], s=150, linewidth=0.5, edgecolor="black")


# -----------------------------------------------------------------------------
# Lowell static mean vs final positions
# -----------------------------------------------------------------------------
df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_upper_stats_static_mean.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_upper_stats_static_final.csv", index_col=False)

df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_static_final.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_static_mean.csv", index_col=False)

# Convert datetimes
df1["date"] = pd.to_datetime(df1["date"].astype(str), format="%Y-%m-%d")
df2["date"] = pd.to_datetime(df2["date"].astype(str), format="%Y-%m-%d")

# Create empty data frame
df3 = pd.DataFrame()
df3["date"] = df1["date"]
df3["delta"] = df1["distance"] - df2["distance"]

df4 = pd.DataFrame()
df4["date"] = df1["date"]
df4["delta"] = df1["distance"] - df2["distance"]



# Daily displacement
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="date", y="delta", data=df3, s=50, label="Lowell Upper")
sns.scatterplot(x="date", y="delta", data=df4, s=50, label="Lowell Corner")
ax.set(xlabel=None, ylabel="Static Mean - Final Delta (cm)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_static_mean_final_delta.png", dpi=dpi, transparent=False, bbox_inches="tight")




# -----------------------------------------------------------------------------
# Lowell static vs kinematic
# -----------------------------------------------------------------------------
df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_upper_stats_static_final.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_upper_stats_kinematic.csv", index_col=False)

df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_static_final.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_kinematic.csv", index_col=False)


# Convert datetimes
df1["date"] = pd.to_datetime(df1["date"].astype(str), format="%Y-%m-%d")
df2["date"] = pd.to_datetime(df2["date"].astype(str), format="%Y-%m-%d")

# Create empty data frame
df3 = pd.DataFrame()
df3["date"] = df1["date"]
df3["delta"] = df1["distance"] - df2["distance"]

# Create empty data frame
df4 = pd.DataFrame()
df4["date"] = df1["date"]
df4["delta"] = df1["distance"] - df2["distance"]
    

# Daily displacement
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="date", y="distance", data=df1, color="#0173b2", errorbar=None, label="Static Mean")
sns.lineplot(x="date", y="distance", data=df2, color="#de8f05", errorbar=None, label="Kinematic Mean")
ax.set(xlabel=None, ylabel="Static - Kinematic Δ (cm)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)

# Delta
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="date", y="delta", data=df3, s=50, label="Lowell Upper")
sns.scatterplot(x="date", y="delta", data=df4, s=50, label="Lowell Corner")
ax.set(xlabel=None, ylabel="Static - Kinematic Δ (cm)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_static_kinematic_delta.png", dpi=dpi, transparent=False, bbox_inches="tight")






# -----------------------------------------------------------------------------
# Lowell static vs kinematic
# -----------------------------------------------------------------------------
df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_upper_stats_static_final.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_upper_stats_kinematic.csv", index_col=False)

df1 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_static_final.csv", index_col=False)
df2 = pd.read_csv("/Users/adam/Desktop/gnss/data/statistics/lowell_corner_stats_kinematic.csv", index_col=False)

df1.columns

# Convert datetimes
df1["date"] = pd.to_datetime(df1["date"].astype(str), format="%Y-%m-%d")
df2["date"] = pd.to_datetime(df2["date"].astype(str), format="%Y-%m-%d")

# Create empty data frame
df3 = pd.DataFrame()
df3["date"] = df1["date"]
df3["lat1"] = df1["latitude_decimal_degree"] 
df3["lon1"] = df1["longitude_decimal_degree"]
df3["lat2"] = df2["latitude_decimal_degree"] 
df3["lon2"] = df2["longitude_decimal_degree"]

# Initialize pyproj with appropriate ellipsoid
geodesic = pyproj.Geod(ellps="WGS84")
    
# Calculate forward azimuth and great circle distance between modelled coordinates
direction, back_azimuth, df3["distance"] = geodesic.inv(df3["lon1"].tolist(), 
                                                       df3["lat1"].tolist(),
                                                       df3["lon2"].tolist(), 
                                                       df3["lat2"].tolist())
df3["distance"] = df3["distance"] * 100


# Create empty data frame
df4 = pd.DataFrame()
df4["date"] = df1["date"]
df4["delta"] = df1["distance"] - df2["distance"]
df4["lat1"] = df1["latitude_decimal_degree"] 
df4["lon1"] = df1["longitude_decimal_degree"]
df4["lat2"] = df2["latitude_decimal_degree"] 
df4["lon2"] = df2["longitude_decimal_degree"]

# Calculate forward azimuth and great circle distance between modelled coordinates
direction, back_azimuth, df4["distance"] = geodesic.inv(df4["lon1"].tolist(), 
                                                       df4["lat1"].tolist(),
                                                       df4["lon2"].tolist(), 
                                                       df4["lat2"].tolist())

df4["distance"] = df4["distance"] * 100

# Delta
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="date", y="speed", data=df1, label="Lowell Upper Speed")
sns.lineplot(x="date", y="speed", data=df2, label="Lowell Corner Speed")
#sns.scatterplot(x="date", y="distance", data=df3, s=25, label="Lowell Upper Delta")
#sns.scatterplot(x="date", y="distance", data=df4, s=25, label="Lowell Corner Delta")
ax.set(xlabel=None, ylabel="Static - Kinematic Δ (cm)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_static_kinematic_delta_position.png", dpi=dpi, transparent=False, bbox_inches="tight")


# Delta
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="date", y="speed", data=df1, label="Lowell Upper Speed")
sns.lineplot(x="date", y="speed", data=df2, label="Lowell Corner Speed")
sns.lineplot(x="date", y="distance", data=df3, label="Lowell Upper Delta")
sns.lineplot(x="date", y="distance", data=df4,  label="Lowell Corner Delta")
ax.set(xlabel=None, ylabel="Static - Kinematic Δ (cm)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
sns.despine()
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.35), ncol=2)
plt.savefig(path_figures + "lowell_static_kinematic_delta_position.png", dpi=dpi, transparent=False, bbox_inches="tight")


df4["speed"] = df2["speed"]
df4["displacement"] = df2["distance"]

import seaborn as sns

fig, ax = plt.subplots(figsize=(10,6))
ax.grid(ls="dotted")
sns.regplot(x="displacement", y="distance", data=df4)
ax.set(xlabel="Speed (cm d-1)", ylabel="Distance (cm)")

plt.savefig(path_figures + "speed_displacement_regplot.png", dpi=dpi, transparent=False, bbox_inches="tight")


