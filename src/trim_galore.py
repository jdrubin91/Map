__author__ = 'Jonathan Rubin'

import os

def run(trimdir,newpath):
    output = newpath + 'trimmed/'
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            os.system(trimdir + "trim_galore -o " + output + " " + newpath + file1)
    for file1 in os.listdir(output):
        if 'fq' in file1.split('.')[-1]:
            os.system("mv " + output + file1 + " " + output + file1.split('.')[:-1] + ".fastq")

    return output