__author__ = "Jonathan Rubin"

import os
import time

def run(job,tempdir):
    ID = list()
    with open(job) as F:
        for line in F:
            if 'pando' in line:
                ID.append(line.strip())
    boolean = True
    print "Checking jobs..."
    while boolean:
        for x in range (0,3):  
            b = "Still Running" + "." * x
            print "/r", b
            time.sleep(1)
        time.sleep(7)
        for item in ID:
            os.system("qstat " + item + " &> " + tempdir + "/" + item + "_status.txt")
        status = list()
        for statusfile in [i for i in os.listdir(tempdir) if "_status.txt" in i]:
            with open(tempdir + "/" + statusfile) as F:
                i = 0
                for line in F:
                    i += 1
                status.append(i)
            os.system("rm " + tempdir + "/" + statusfile)
        boolean = sum(status) > 0