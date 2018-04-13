__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, samdir, tempdir, genome, boolean=True):
    outfile = open(scriptdir + 'runbowtiedir.sbatch', 'w')
    outfile.write("od=" + samdir + "\n")
    outfile.write("indir=" + indir + "\n")
    if boolean:
        outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename`\n")
    if not boolean:
        outfile.write("entry=${entry}."+genome.split('/')[-1].split('.')[0]+"\n")
    outfile.write("echo $entry\n")
    outfile.write("fq1=$entry\n")
    outfile.write("ofile=${entry}.bowtie2\n")
    outfile.write("echo $ofile\n")
    outfile.write("echo ${odir}${ofile}.sam\n")
    outfile.write("sbatch -J ${ofile}bowtiemap --export=fastq1pathandfile=$pathandfilename,outdir=$od,outfile=$ofile " + scriptdir + "/bowtieafastq.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "runbowtiedir.sbatch > " + tempdir + "/Job_ID.txt")