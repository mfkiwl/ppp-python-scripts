from subprocess import Popen, PIPE
import os
import time
import glob
import logging

logging.basicConfig(filename="logtest.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger("csrs_ppp")

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
    p = Popen([command], shell=True, stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode != 0: 
       logger.debug("Popen failed {} {} {}".format(p.returncode, output, error))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update(
            [p for p in processes if p.poll() is not None])

# Check if all child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()
