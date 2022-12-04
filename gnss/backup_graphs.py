#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:09:00 2022

@author: adam
"""

import datetime




print('{}'.format(datetime.datetime.strftime()))




# Radiation vs battery voltage
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.grid(ls="dotted")
sns.lineplot(x="dts", y="Kdn", data=df, color="#0173b2", alpha=0.8)
ax1.set(ylabel="Downwelling shortwave (W/m^2)", xlabel=None)
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45, horizontalalignment="center")
ax2 = plt.twinx()
sns.lineplot(x='datetime', y='voltage', data=df1, errorbar=None, color="#de8f05", lw=lw, label="Qakuqtaqtujut", alpha=0.8)
#sns.lineplot(x='datetime', y='voltage', data=df2, errorbar=None, color="#029e73", lw=lw, label="Pullataujaq")
ax2.set(xlabel=None, ylabel="Voltage (V)", ylim=(13,16))
# Save figure
fig.savefig("/Users/Adam/Desktop/sw_voltage.png", dpi=dpi, transparent=False, bbox_inches="tight")


fig, ax1 = plt.subplots(figsize=(10,6))
ax1.grid(ls="dotted")
sns.lineplot(x="dts", y="Z_invert", data=df, alpha=0.8, color="#0173b2",)
ax1.set(ylabel="Solar elevation angle (°)", xlabel=None)
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45, horizontalalignment="center")
ax2 = plt.twinx()
sns.lineplot(x='datetime', y='voltage', data=df1, errorbar=None, color="#de8f05", lw=lw, label="Qakuqtaqtujut", alpha=0.8)
#sns.lineplot(x='datetime', y='voltage', data=df2, errorbar=None, color="#029e73", lw=lw, label="Pullataujaq")
ax2.set(xlabel=None, ylabel="Voltage (V)", ylim=(13,15.5))
# Save figure
fig.savefig("/Users/Adam/Desktop/angle_voltage.png", dpi=dpi, transparent=False, bbox_inches="tight")





