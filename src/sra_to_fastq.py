__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runsradump.sh', 'w')
    outfile.write("indir=" + fullpath + "\n")
    outfile.write("for pathandfilename in `ls $indir*.sra`; do\n")
    outfile.write("entry=`basename $pathandfilename .sra`\n")
    outfile.write("infilename=$pathandfilename\n")
    outfile.write("qsub -v infile=$infilename -N sradump${entry} " + scriptdir + "/sradump.sh\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runsradump.sh")