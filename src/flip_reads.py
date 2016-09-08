__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runflipfastq.sh', 'w')
    outfile.write("od=" + fullpath + "flipped/\n")
    outfile.write("indir=" + fullpath + "\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename .fastq`\n")
    outfile.write("echo $entry\n")
    outfile.write("ofile=${entry}.flip.fastq\n")
    outfile.write("echo $ofile\n")
    outfile.write("qsub -v infile=$pathandfilename,outfile=$ofile,outdir=$od -N ${ofile}flip " + scriptdir + "/flipfastq.sh\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runflipfastq.sh > " + tempdir + "/Job_ID.txt")
    
    return fullpath + 'flipped/'