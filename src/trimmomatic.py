__author__ = 'Jonathan Rubin'

import os

def run(trimmomaticdir,newpath):
    output = newpath + 'trimmed/'
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1 + " ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36")

    return output