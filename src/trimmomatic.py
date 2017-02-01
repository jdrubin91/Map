__author__ = 'Jonathan Rubin'

import os

def run(trimmomaticdir,newpath):
    output = newpath + 'trimmed/'
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            # os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1 + " ILLUMINACLIP:Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 CROP:100 HEADCROP:50")
            os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1 + " MINLEN:36 CROP:100 HEADCROP:50")

    return output