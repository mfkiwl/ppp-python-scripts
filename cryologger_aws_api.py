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

# Qakuqtaqtujut
response = requests.get("https://api.cryologger.org/aws?imei=300434063398110&records=3000")
#response = requests.get("https://api.cryologger.org/aws?imei=300434063398110&field=voltage&records=10000")
df1 = pd.read_json(response.text)

# Pullataujaq
response = requests.get("https://api.cryologger.org/aws?imei=300434063396360&records=3000")
#response = requests.get("https://api.cryologger.org/aws?imei=300434063396360&field=transmit_duration&records=6000")
df2 = pd.read_json(response.text)

# Convert unixtime to datetime
df1["datetime"] = pd.to_datetime(df1["unixtime"], unit="s")
df2["datetime"] = pd.to_datetime(df2["unixtime"], unit="s")

# Subset by datetime
df1 = df1[(df1["datetime"] > "2022-05-09 00:00")]
df2 = df2[(df2["datetime"] > "2022-05-09 00:00")]

# Remove 0 s transmit durations
df1.loc[df1["transmit_duration"] == 0, "transmit_duration"] = np.nan
df2.loc[df2["transmit_duration"] == 0, "transmit_duration"] = np.nan

# Remove voltages less than 12 V
df1.loc[df1["voltage"] < 12, "voltage"] = np.nan
df2.loc[df2["voltage"] < 12, "voltage"] = np.nan

# Convert wind speed from m/s to km/h
df1["wind_speed"] *= 3.6 
df2["wind_speed"] *= 3.6

# -----------------------------------------------------------------------------
# Plot
# -----------------------------------------------------------------------------

# Voltage
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="voltage", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="voltage", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Voltage (V)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "voltage.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Temperature Internal (°C)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="temperature_int", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="temperature_int", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Temperature (°C)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_int.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Temperature External (°C)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="temperature_ext", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="temperature_ext", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Temperature External (°C)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_ext.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Humidity (%)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="humidity_ext", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="humidity_ext", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Humidity External (%)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_ext.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Wind Speed
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="wind_speed", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="wind_speed", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Wind Speed (km/h)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_int.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Wind Direction (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="wind_direction", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="wind_direction", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Wind Direction (°)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "temperature_int.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Pitch (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="pitch", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="pitch", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Pitch (°)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "pitch.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Roll (°)
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="roll", data=df1, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="roll", data=df2, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Roll (°)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "roll.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Transmit Duration
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.scatterplot(x="datetime", y="transmit_duration", data=df1, label="Qakuqtaqtujut")
sns.scatterplot(x="datetime", y="transmit_duration", data=df2, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Transmit Duration (s)")
plt.xticks(rotation=45, horizontalalignment="right")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "transmit_duration.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Voltage
fig, ax = plt.subplots(figsize=(10,5))
ax.grid(ls="dotted")
sns.lineplot(x="datetime", y="min", data=df3, errorbar=None, lw=lw, label="Qakuqtaqtujut")
sns.lineplot(x="datetime", y="min", data=df4, errorbar=None, lw=lw, label="Pullataujaq")
ax.set(xlabel=None, ylabel="Voltage Min (V)")
plt.xticks(rotation=45, horizontalalignment="center")
ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)) 
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), title="Station")
plt.savefig(path_figures + "voltage_min.png", dpi=dpi, transparent=False, bbox_inches="tight")
