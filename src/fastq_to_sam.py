__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runbowtiedir.sh', 'w')
    outfile.write("od=" + fullpath + "flipped/bowtie2/\n")
    outfile.write("indir=" + fullpath + "flipped/\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename`\n")
    outfile.write("echo $entry\n")
    outfile.write("fq1=$entry\n")
    outfile.write("ofile=${entry}bowtie2\n")
    outfile.write("echo $ofile\n")
    outfile.write("echo ${odir}${ofile}.sam\n")
    outfile.write("qsub -v fastq1pathandfile=$pathandfilename,outdir=$od,outfile=$ofile -N ${ofile}bowtiemap " + scriptdir + "/bowtieafastq.sh\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runbowtiedir.sh")