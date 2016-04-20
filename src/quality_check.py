__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runqual.sh', 'w')
    outfile.write("id=" + fullpath + "\n")
    outfile.write("for pathandfilename in `ls $id*.fastq`; do")
    outfile.write("entry=`basename $pathandfilename`")
    outfile.write("qsub -v filename=$entry,indir=$id -N ${fn1}qual " + scriptdir + "/qual.sh")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runqual.sh")