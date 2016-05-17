__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, newpath):
    os.system("python " + scriptdir + "/igvtoolstile_2.py " + newpath + "genomecoveragebed/fortdf/")
    os.system("bash " + newpath + "genomecoveragebed/fortdf/igvtoolstile.sh")