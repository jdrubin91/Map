__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, newpath):
    os.system("python " + scriptdir + "/readcount_corrected_geneomeBedgraphs.py " + newpath[0:-1])