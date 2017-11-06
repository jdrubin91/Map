__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, newpath, genome):
    os.system("python " + scriptdir + "/igvtoolstile_2.py " + genome + " " + newpath + "genomecoveragebed/fortdf/")
    os.system("bash " + newpath + "genomecoveragebed/fortdf/igvtoolstile.sbatch")