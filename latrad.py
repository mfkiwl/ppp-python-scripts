#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 20:27:01 2022

@authors: Adam Garbo, Derek Mueller

latrad.py - Calculate sun angles and flux density based on latitude

Equations from Appendix A in Oke, TR 1987. Boundary Layer Climates
Due to refraction, Kdown at low solar angles are not correct (Z<80degrees)

Kex = Shortwave Radiation at the top of the atmosphere
Kdn = Direct Shortwave Solar Radiation on a horizontal surface
m = path length correction factor
Z = the zenith angle
delta = solar declination
h = hour angle
omega = azimuth angle

civil twilight = 6deg below horizon
astronomical twilight = 18deg below horizon
Shortwave Radiation is 150 to 3000 nm

Improvments to the code could be made
See: https://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/how-solar-radiation-is-calculated.htm
# Also, can include calculations for solar panel power. See TODO below


"""

import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Configure Seaborn styles
sns.set_theme(style="ticks")
sns.set_context("talk")  # Options: talk, paper, poster

# Path to figures
path_figures = "/Volumes/GoogleDrive/My Drive/Cryologger/Python/latrad/"

# Figure DPI
dpi = 300

# Parameters
lat = 69.3725  # Latitude
lon = -81.8246  # Longitude
solar_const = 1367.0  # Solar constant (W/m^2)
atm_trans = 0.84  # Atmospheric transmissivity

# Start and end dates
# dt1 = datetime(2022, 1, 1)  # Start time
# dt2 = datetime(2022, 12, 31)  # End time
dt1 = pd.to_datetime("2022-01-01 00:00")
dt2 = pd.to_datetime("2022-12-31 23:00")

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def getDelta(doy):
    # Solar declination
    return -23.4 * (np.cos(np.radians(360 * (doy + 10) / 365)))


def getZ(lat, delta):
    # Zenith Angle
    return np.degrees(
        np.arccos(
            np.sin(np.radians(lat)) * np.sin(np.radians(delta))
            + np.cos(np.radians(lat))
            * np.cos(np.radians(delta))
            * np.cos(np.radians(h))
        )
    )


def getOmega(lat, delta, h, Z):
    # Azimuth angle
    cos_omega = (
        (np.sin(np.radians(delta)) * np.cos(np.radians(lat)))
        - (np.cos(np.radians(delta)) * np.sin(np.radians(lat)) * np.cos(np.radians(h)))
    ) / np.sin(np.radians(Z))
    omega = np.degrees(np.arccos(cos_omega))
    omega[np.where(h < 0)] = 360 - omega[np.where(h < 0)]
    omega[np.where(h == 180)] = 0  # NaNs produced when h is 180 or 0
    omega[np.where(h == 0)] = 180  # NaNs produced when h is 180 or 0
    return omega


def getH(lat, delta):
    # Hour angle at rise/set
    # https://en.wikipedia.org/wiki/Sunrise_equation
    cosH = -1 * np.tan(np.radians(lat)) * np.tan(np.radians(delta))
    cosH[np.where(cosH > 1)] = 1
    cosH[np.where(cosH < -1)] = -1
    return np.degrees(np.arccos(cosH))


def getKex(Z, solarconst):
    # Determine the shortwave flux at the top of atm.
    Kex = solarconst * np.cos(np.radians(Z))
    Kex[np.where(Kex < 0)] = 0
    return Kex


def getKdn(Kex, Z, atmtrans):
    # Determine the shortwave flux at the surface of Earth
    m = 1 / np.cos(np.radians(Z))  # path length correction factor
    Kdn = Kex * atmtrans ** m  # Shortwave flux at surface on the flat ground
    return Kdn


def time2h(hod):
    # Provide hour of day in solar time and it will return the hour angle that corresponds
    return 15 * (12 - hod)


def h2time(h):
    # Provide hour angle and it will return the time that corresponds
    return (h / -15) + 12


def getRise(lat, doy):
    # Get sunrise solar time
    return h2time(getH(lat, getDelta(doy)))


def getSet(lat, doy):
    # Get sunset solar time
    return (12 - getRise(lat, doy)) + 12


def getDaylength(lat, doy):
    # Get day length in hrs
    return getSet(lat, doy) - getRise(lat, doy)


def getNumberOfDaysBelowThreshold(lat, threshold):
    # Number of days per year where daylight is less than or equal to threshold
    # sum(getDaylength(lat,1:366) <= threshold)
    return


# -----------------------------------------------------------------------------
# Run the code
# -----------------------------------------------------------------------------

# Create a vector of date/times - start and stop when you want
dts = pd.date_range(start=dt1, end=dt2, freq="H")
doy = dts.day_of_year.values  # Get day of year
hod = dts.hour.values  # Get hour of day
delta = getDelta(doy)  # Solar declination
h = time2h(hod)  # Hour angle (Note: 0 and 24 issues?)
Z = getZ(lat, getDelta(doy))
Kex = getKex(Z, solar_const)
Kdn = getKdn(Kex, Z, atm_trans)

# Pandas version
# Create an empty dataframe
df = pd.DataFrame()
df["dts"] = pd.date_range(start=dt1, end=dt2, freq="H")
df["doy"] = dts.day_of_year.values
df["hod"] = dts.hour.values
df["delta"] = getDelta(doy)  # Solar declination
df["h"] = time2h(hod)  # Hour angle (Note: 0 and 24 issues?)
df["Z"] = getZ(lat, getDelta(doy))
df["Kex"] = getKex(Z, solar_const)
df["Kdn"] = getKdn(Kex, Z, atm_trans)

df["Z_invert"] = 90 - df["Z"]

# Create date range array
doy = pd.date_range(start=dt1, end=dt2, freq="D").day_of_year.values

# Create an empty dataframe
df2 = pd.DataFrame()
df2["date"] = pd.date_range(start=dt1, end=dt2, freq="D")
df2["doy"] = pd.date_range(start=dt1, end=dt2, freq="D").day_of_year.values
df2["day_length"] = getDaylength(lat, doy)

# Count number of days with less than a specified number of daylight hours
threshold = 5  # Daylight hour threshold
df2[df2["day_length"] <= threshold].count()

# -----------------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------------

# Plot interpolation alongside total number of observations
fig, ax = plt.subplots(figsize=(12, 6))
ax.grid(ls="dotted")
sns.lineplot(x="dts", y="Z_invert", data=df, alpha=0.75)
sns.despine()
ax.set(ylabel="Solar elevation angle (°)", xlabel=None)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.title("Igloolik, Nunavut")
fig.savefig(path_figures + "Z_elev.png", dpi=dpi, transparent=False, bbox_inches="tight")


# Plot interpolation alongside total number of observations
fig, ax = plt.subplots(figsize=(12, 6))
ax.grid(ls="dotted")
sns.lineplot(x="dts", y="Kdn", data=df)
sns.despine()
ax.set(ylabel="Downwelling shortwave (W/m^2)", xlabel="Date")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.title("Igloolik, Nunavut")
fig.savefig(path_figures + "shortwave.png", dpi=dpi, transparent=False, bbox_inches="tight")

# Day length
fig, ax = plt.subplots(figsize=(12, 6))
ax.grid(ls="dotted")
sns.lineplot(x="doy", y="day_length", data=df2)
sns.despine()
ax.set(xlabel="Day of Year", ylabel="Day Length (h)")
plt.title("Igloolik, Nunavut")
fig.savefig(path_figures + "day_length.png", dpi=dpi, transparent=False, bbox_inches="tight")
















