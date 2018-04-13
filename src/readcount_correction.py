__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, outdir):
    os.system("python " + scriptdir + "readcount_corrected_geneomeBedgraphs.py " + indir + " " + outdir)