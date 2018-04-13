__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, tempdir, genome, e_and_o, email):
    os.system("python " + scriptdir + "igvtoolstile_2.py " + genome + " " + indir + " " + e_and_o + " " + email)
    os.system("sbatch " + indir + "igvtoolstile.sbatch > " + tempdir + "/Job_ID.txt")