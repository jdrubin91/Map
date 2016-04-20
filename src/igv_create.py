__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath):
    os.system("python " + scriptdir + "/igvtoolstile_2.py " + fullpath + "flipped/bowtie2/sortedbam/genomecoveragebed/fortdf/")
    os.system("bash " + fullpath + "flipped/bowtie2/sortedbam/genomecoveragebed/fortdf/igvtoolstile.sh")