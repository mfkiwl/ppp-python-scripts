#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 09:05:51 2022

@author: Adam Garbo

https://scitools.org.uk/cartopy/docs/latest/tutorials/understanding_transform.html

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import cm
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.ticker import (LongitudeFormatter, 
                                LatitudeFormatter,
                                LongitudeLocator,
                                LatitudeLocator)

# Path
path_data = "/Users/adam/Downloads/IBCAO_v4_2_200m_16_tiled_netCDF/"

# Load data
ds = xr.open_dataset("/Users/adam/Downloads/IBCAO_v4_2_400m.nc")

# Load data with slicing
ds = xr.open_dataset("/Users/adam/Downloads/IBCAO_v4_2_400m.nc").sel(x=slice(-2902500, 0),y=slice(-2902500, 500000))
ds.z.values.min()

# Select underwater values only
ds0 = ds.where(ds.z.values <= 0) 

# Create a Stamen terrain background instance
stamen_terrain = cimgt.Stamen("terrain-background")


# North Polar Stereo map 
plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.NorthPolarStereo(true_scale_latitude=75))
#ax.set_extent([-80, -60, 75, 82.5])
cs = plt.contour(ds0.x, ds0.y, ds0.z, 20, zorder=1)
#cbar = plt.colorbar(cs, location="right")
ax.gridlines(ls="dotted")
ax.coastlines()
#ax.add_image(stamen_terrain, 5)
ax.add_feature(coast)
plt.savefig(path_data + "test0.png", dpi=200, transparent=False, bbox_inches='tight')

# Orthographic map 
plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.Orthographic(-70,75))
#ax.set_extent([-80, -60, 75, 82.5])
cs = plt.contour(ds.x, ds.y, ds.z, transform=ccrs.NorthPolarStereo())
# = plt.colorbar(cs, location="right")
ax.gridlines(ls="dotted")
ax.coastlines()
plt.savefig(path_data + "test5.png", dpi=300, transparent=False, bbox_inches='tight')


# Orthographic map to illustrate misalignment
plt.figure(figsize=(10,10))
ax = plt.axes(projection=ccrs.Orthographic(-70,75))
ax.set_extent([-85, -50, 60, 82.5])
cs = plt.contourf(ds.x, ds.y, ds.z, 20, transform=ccrs.NorthPolarStereo(true_scale_latitude=75)) # Specifiy true scale latitude to avoid misalignment
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  color="black", alpha=0.25, linestyle="dotted",
                  x_inline=False, y_inline=False)
gl.top_labels = False
gl.right_labels = False
gl.rotate_labels = False
gl.xlocator = mticker.FixedLocator(np.arange(-180,0,5))
gl.ylocator = mticker.FixedLocator(np.arange(40,90,2))
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()
plt.savefig(path_data + "misalignmentx.png", dpi=300, transparent=False, bbox_inches='tight')
