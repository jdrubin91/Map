__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath):
    print "python " + scriptdir + "/readcount_corrected_geneomeBedgraphs.py " + fullpath + "flipped/bowtie2/sortedbam"
    os.system("python " + scriptdir + "/readcount_corrected_geneomeBedgraphs.py " + fullpath + "flipped/bowtie2/sortedbam")