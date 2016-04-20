__author__ = "Jonathan Rubin"

import os
import time

def run(jobfile, tempdir):
    ID = open(jobfile).readline()
    boolean = True
    while boolean:
        time.sleep(120)
        os.system("qstat " + ID + " > " + tempdir + "/status.txt")
        i = 0
        for line in open(tempdir + "/status.txt"):
            i += 1
        boolean = i > 0
        