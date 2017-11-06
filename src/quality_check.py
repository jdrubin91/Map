__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, newpath, tempdir):
    outfile = open(scriptdir + '/runqual.sbatch', 'w')
    outfile.write("id=" + newpath + "\n")
    outfile.write("for pathandfilename in `ls $id*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename`\n")
    outfile.write("sbatch -v filename=$entry,indir=$id -N ${fn1}qual " + scriptdir + "/qual.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runqual.sbatch > " + tempdir + "/Job_ID.txt")
    
    return tempdir + "/Job_ID.txt"