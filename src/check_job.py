__author__ = "Jonathan Rubin"

import os
import time

def run(job,tempdir):
    ID = list()
    with open(job) as F:
        for line in F:
            ID.append(line)
    boolean = True
    while boolean:
        #time.sleep(120)
        for item in ID:
            os.system("qstat " + item + " > " + tempdir + "/" + item + "_status.txt")
        status = list()
        for statusfile in [i for i in os.listdir(tempdir) if "_status.txt" in i]:
            with open(statusfile) as F:
                i = 0
                for line in F:
                    i += 1
                status.append(i)
        boolean = sum(status) > 0
        