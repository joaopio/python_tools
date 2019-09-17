# !/usr/bin/env python

__doc__ = \
    '''
    
'''

__version__ = '0.1'

__authors__ = [
    "Version 0.1: Joao Pio <joao-t-pio@telecom.pt>"
]

import os
import time
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

if __name__ == "__main__":

    total_header = ["DATETIME", "PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    header = ["PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
    columns = ["PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+"]
    indexes = ["DATETIME", "PID"]

    filter_process = "python"
    # filter_process = "watchdog"
    frames = 6
    interval = 1

    total_index = pd.MultiIndex(levels=[[], []], codes=[[], []], names=[u'DATETIME', u'COMMAND'])

    total_run_df = pd.DataFrame(columns=list(columns), index=total_index)

    for frame in range(0, frames, 1):

        # Launch process "top" with batch mode and one iteration to avoid locking the program
        process = os.popen('top -b -n 1 -c | grep "{}"'.format(filter_process))
        preprocessed = process.read()
        process.close()

        # Obtain current time
        frame_time = datetime.now()

        lines = preprocessed.split("\n")

        for line in lines:
            if len(line) == 0:
                continue

            line = line.split()
            # In case there are spaces in the command column, concat them
            if len(line) != len(header):
                temp_line = line[:len(header)-1]
                temp_line.append(" ".join(line[len(header)-1:]))
                line = temp_line

            line = dict(zip(header, line))
            command = line.pop("COMMAND")

            print("COMMAND - {0}: {1}".format(command, line.values()))

            total_run_df.loc[(frame_time, command), :] = line.values()

        time.sleep(interval)

    total_run_df = total_run_df.dropna()

    # print (pd.to_numeric(total_run_df["%MEM"]))
    # print (pd.to_numeric(total_run_df["VIRT"]))
    # print(pd.to_numeric(total_run_df["RES"]))

    print(total_run_df["RES"])
    print(total_run_df["RES"].unstack())

    # pd.to_numeric(total_run_df["%MEM"]).plot(kind='line', subplots=True)
    pd.to_numeric(total_run_df["RES"])\
        .unstack()\
        .plot(kind='line', subplots=False)

    plt.show()
