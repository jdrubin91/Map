__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runbowtiedir.sh', 'w')
    outfile.write("od=" + fullpath + "flipped/bowtie2/")
    outfile.write("indir=" + fullpath + "flipped/")
    outfile.write("mkdir -p $od")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do")
    outfile.write("entry=`basename $pathandfilename`")
    outfile.write("echo $entry")
    outfile.write("fq1=$entry")
    outfile.write("ofile=${entry}bowtie2")
    outfile.write("echo $ofile")
    outfile.write("echo ${odir}${ofile}.sam")
    outfile.write("qsub -v fastq1pathandfile=$pathandfilename,outdir=$od,outfile=$ofile -N ${ofile}bowtiemap " + scriptdir + "/bowtieafastq.sh")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runbowtiedir.sh > " + tempdir + "/Job_ID.txt")
    
    return tempdir + "/Job_ID.txt"