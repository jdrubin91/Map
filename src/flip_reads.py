__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runflipfastq.sh', 'w')
    outfile.write("od=" + fullpath + "flipped/")
    outfile.write("indir=" + fullpath)
    outfile.write("mkdir -p $od")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do")
    outfile.wrtie("entry=`basename $pathandfilename .fastq`")
    outfile.write("echo $entry")
    outfile.write("ofile=${entry}.flip.fastq")
    outfile.write("echo $ofile")
    outfile.write("qsub -v infile=$pathandfilename,outfile=$ofile,outdir=$od -N ${ofile}flip " + scriptdir + "/flipfastq.sh")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runflipfastq.sh")