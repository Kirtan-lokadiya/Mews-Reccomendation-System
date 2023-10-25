# HERE WE ARE FIRST CREATING OUR LOGGING FUNCTION

import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(level= logging.INFO, format= logging_str, handlers= [
    logging.FileHandler(log_filepath),    # will save all my logs in the runnig_logs.log
    logging.StreamHandler(sys.stdout)     # will print these logs on the terminal
])

logger = logging.getLogger('News_Reccomendation_Logger')
