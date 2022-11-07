import subprocess
import os
import time
import glob

input_path = "/tank/SCRATCH/agarbo/gnss/belcher_lower/RINEX/"
output_path = "/tank/SCRATCH/agarbo/gnss/belcher_lower/ppp/"
files = sorted(glob.glob(input_path + "*.obs", recursive=True))

processes = set()
max_processes = 2

for file in files:
    command = "python3 csrs_ppp_auto.py --user_name adam.garbo@carleton.ca --results_dir {} --rnx {}".format(output_path, file)
    print(command)
    processes.add(subprocess.Popen([command],shell=True))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update(
            [p for p in processes if p.poll() is not None])
# Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()