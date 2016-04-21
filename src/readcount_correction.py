__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath):
    os.system("python " + scriptdir + "/readcount_corrected_geneomeBedgraphs.py " + fullpath + "flipped/bowtie2/sortedbam")