__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runsradump.sh', 'w')
    outfile.write("indir=" + fullpath + "\n")
    outfile.write("for pathandfilename in `ls $indir*.sra`; do")
    outfile.write("entry=`basename $pathandfilename .sra`")
    outfile.write("infilename=$pathandfilename")
    outfile.write("qsub -v infile=$infilename -N sradump${entry} " + scriptdir + "/sradump.sh")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runsradump.sh > " + tempdir + "/Job_ID.txt")
    
    return tempdir + "/Job_ID.txt"