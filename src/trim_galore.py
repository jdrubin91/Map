__author__ = 'Jonathan Rubin'

import os

def run(trimdir,newpath):
    for file1 in os.listdir(newpath):
        os.system(trimdir + newpath + "trim_galore " + file1)