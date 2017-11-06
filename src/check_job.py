__author__ = "Jonathan Rubin"

import os
import sys
import time

def run(job,tempdir):
    ID = list()
    #Requires a 'job' file where all job names are stored
    with open(job) as F:
        for line in F:
            #Append job names to list 'ID'
            if 'Submitted batch job' in line:
                ID.append(line.strip('\n').split(' ')[-1])
                print ID
    boolean = True
    while boolean:
        #Check all job IDs using qstat. If job is done, status.txt will be empty
        for item in ID:
            os.system("qstat " + item + " > " + tempdir + "/" + item + "_status.txt 2> " + tempdir + "/error_storage.err")
        status = list()
        #Check all status.txt files for all jobs. If all status.txt files are empty, all jobs are done
        for statusfile in [i for i in os.listdir(tempdir) if "_status.txt" in i]:
            with open(tempdir + "/" + statusfile) as F:
                i = 0
                for line in F:
                    i += 1
                status.append(i)
            os.system("rm " + tempdir + "/" + statusfile)
        boolean = sum(status) > 0
        #If there are still jobs running, print statement, then wait to check jobs again
        if boolean:
            for j in range(3):
                #Clears previous print statement
                print "\r",
                sys.stdout.write("\033[K")
                #Prints x Job(s) Still Running...
                for x in range (4):
                    b = str(sum([1 for i in status if i>0])) + " Job(s) Still Running" + "." * x
                    #"/r" moves cursor to beginning
                    print "\r",b,
                    sys.stdout.flush()
                    time.sleep(1)
                    
    print "\r",
    sys.stdout.write("\033[K")
        
