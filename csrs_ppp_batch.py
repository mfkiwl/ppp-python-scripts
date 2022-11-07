import subprocess
import os
import time
import glob

# Set paths
input_path = "/tank/SCRATCH/agarbo/gnss/belcher_upper/RINEX/"
output_path = "/tank/SCRATCH/agarbo/gnss/belcher_upper/ppp/"

# Search for all RINEX .obs files
files = sorted(glob.glob(input_path + "*.obs", recursive=True))

# Set number of concurrent processes
processes = set()
max_processes = 4

# Loop through and process each RINEX .obs file
for file in files:
    command = "python3 csrs_ppp_auto.py --user_name adam.garbo@carleton.ca --epoch 2010-01-01 --mode Static --output_pdf lite --get_max 180 --results_dir {} --rnx {}".format(output_path, file)
    print(command)
    processes.add(subprocess.Popen([command],shell=True))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update(
            [p for p in processes if p.poll() is not None])

# Check if all child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()