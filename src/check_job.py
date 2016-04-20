__author__ = "Jonathan Rubin"

import os
import time

def run(tempdir, user):
    boolean = True
    while boolean:
        #time.sleep(120)
        os.system("qstat -u " + user + " > " + tempdir + "/status.txt")
        i = 0
        for line in open(tempdir + "/status.txt"):
            i += 1
        boolean = i > 0
        