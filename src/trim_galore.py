__author__ = 'Jonathan Rubin'

import os

def run(trimdir,trimoptions,newpath):
    output = newpath + 'trimmed/'
    os.system("mkdir " + output)
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            os.system(trimdir + "trim_galore -o " + output + " " + trimoptions + newpath + file1)
    for file1 in os.listdir(output):
        if 'fq' in file1.split('.')[-1]:
            os.system("mv " + output + file1 + " " + output + ".".join(file1.split('.')[:-1]) + ".fastq")

    return output