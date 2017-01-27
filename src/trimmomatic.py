__author__ = 'Jonathan Rubin'

import os

def run(trimmomaticdir,newpath):
    output = newpath + 'trimmed/'
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1)

    return output