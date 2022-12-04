#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:25:13 2022

@author: adam
"""

import glob
from subprocess import call
from pathlib import Path

# Import CSV files from folder
input_path = "/tank/SCRATCH/agarbo/GNSS/belcher_lower/"
output_path = input_path + "RINEX/"

# Create output path if required 
try:
    Path(output_path).mkdir(parents=True, exist_ok=False)
except FileExistsError:
    print("{} already exists".format(output_path))
else:
    print("{} folder was created".format(output_path))
    
# Recursively search for .ubx files
files = sorted(glob.glob(input_path + "*.ubx", recursive=True))

# Loop through each file
for file in files:
    program = "convbin"
    arguments = "-od -os -oi -ot"
    output = "-d {}".format(output_path)
    convbin_cmd = "{} {} {} {}".format(program,arguments,output,file)
    call([convbin_cmd],shell=True)
