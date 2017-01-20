__author__ = 'Jonathan Rubin'

import os

def run(trimdir,newpath):
    for file1 in os.listdir(newpath):
        output = newpath + 'trimmed/'
        os.system(trimdir + "trim_galore - o " + output + " " + newpath + file1)

    return output