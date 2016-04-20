__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath):
    os.system("python " + scriptdir + "/millions_mapped.py " + fullpath)