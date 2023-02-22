#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:20:40 2022

@author: adam
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import requests

# -----------------------------------------------------------------------------
# Plotting attributes
# -----------------------------------------------------------------------------

# Seaborn configuration
sns.set_theme(style="ticks")
sns.set_context("talk") # talk, paper, poster

# Set colour palette
sns.set_palette("colorblind")

# Graph attributes
lw = 1
interval = 30
date_format = "%Y-%m-%d"

# Figure DPI
dpi = 300

# -----------------------------------------------------------------------------
# Folder paths
# -----------------------------------------------------------------------------

path = "/Users/adam/Documents/GitHub/cryologger-automatic-weather-station/Software/Python/"

# Data directory
path_data = "/Users/adam/Documents/GitHub/cryologger-automatic-weather-station/Software/Python"

# Figure directory
path_figures = "/Users/adam/Documents/GitHub/cryologger-automatic-weather-station/Software/Python/Figures/"


# -----------------------------------------------------------------------------
# Load and prepare data
# -----------------------------------------------------------------------------

# Station UID
# ALW	73.581863	-83.654776	Arctic Bay, Nunavut	Qakuqtaqtujut
# MPC	73.4802	    -85.6052	Arctic Bay, Nunavut	Pullataujaq
headers = {'x-api-key': "fZ9d7bKQB69Yur74Xmz7i8Rf7o24kpga4PpnGxBF"}

url = "https://api.cryologger.org/aws?uid=NPK"
response = requests.get(url, headers=headers)
df = pd.read_json(response.text)
response.content


url = "https://api.cryologger.org/aws?uid=ALW&uid=MPC&records=200000"
response = requests.get(url, headers=headers)
df = pd.read_json(response.text)

# Convert unixtime to datetime
df["datetime"] = pd.to_datetime(df["unixtime"], unit="s")

# Subset by datetime
df = df[(df["datetime"] > "2023-01-01 00:00")]

#df = df[(df["datetime"] < "2023-01-28 00:00")]

# Remove 0 s transmit durations
df.loc[df["transmit_duration"] == 0, "transmit_duration"] = np.nan

# Remove voltages less than 12 V
df.loc[df["voltage"] < 12.5, "voltage"] = np.nan

# Convert wind speed from m/s to km/h
df["wind_speed"] *= 3.6 

df["wind_gust_speed"] *= 3.6 

df.loc[df["wind_gust_speed"] == 0, "wind_gust_speed"] = np.nan

# -----------------------------------------------------------------------------
# Plot
# -----------------------------------------------------------------------------

# Voltage & Temperature

fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="voltage", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Voltage (V)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "voltage.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Temperature Internal (°C)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="temperature_int", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Temperature (°C)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_int.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Temperature External (°C)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="temperature_ext", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Temperature External (°C)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_ext.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Humidity (%)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="humidity_ext", data=df, errorbar=None, lw=lw, label="Qakuqtaqtujut")
ax.set(xlabel=None, ylabel="Humidity External (%)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_ext.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Wind Speed
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="wind_speed", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Wind Speed (km/h)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "wind_speed.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Wind Gust Speed 
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="wind_gust_speed", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Wind Gust Speed (km/h)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "wind_gust_speed.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Wind Direction (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="wind_direction", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Wind Direction (°)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_int.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Pitch (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="pitch", data=df, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Pitch (°)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
#ax.xaxis.set_major_locator(mdates.DayLocator(interval=7)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "pitch.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Roll (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="roll", data=df, errosrbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Roll (°)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "roll.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Transmit Duration
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="datetime", y="transmit_duration", data=df, hue="uid")
ax.set(xlabel=None, ylabel="Transmit Duration (s)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "transmit_duration.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Voltage
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="min", data=df3, errorbar=None, lw=lw, hue="uid")
ax.set(xlabel=None, ylabel="Voltage Min (V)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "voltage_min.png", dpi=dpi, transparent=False, bbox_inches="tight")



# Add month column

df["month"] = df["datetime"].dt.
df["month"] = pd.to_datetime(df["month"], format='%m').dt.month_name().str.slice(stop=3)

# relationship (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="wind_gust_speed", y="pitch", data=df, hue="month")
ax.set(xlabel="Wind Gust Speed (km/h)", ylabel="Pitch (°)")
plt.xticks(rotation=0, horizontalalignment="right")
#ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
#ax.xaxis.set_major_locator(mdates.DayLocator(interval=7)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Month")
plt.savefig(path_figures + "pitch_gust2.png", dpi=dpi, transparent=False, bbox_inches="tight")




fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="wind_gust_speed", y="roll", data=df, label="Qakuqtaqtujut")
ax.set(xlabel="Wind Gust Speed (km/h)", ylabel="Pitch (°)")
plt.xticks(rotation=0, horizontalalignment="right")
#ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
#ax.xaxis.set_major_locator(mdates.DayLocator(interval=7)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "roll_gust.png", dpi=dpi, transparent=False, bbox_inches="tight")


