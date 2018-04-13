__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, flipdir, tempdir):
    outfile = open(scriptdir + 'runflipfastq.sbatch', 'w')
    outfile.write("od=" + flipdir + "\n")
    outfile.write("indir=" + indir + "\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename .fastq`\n")
    outfile.write("echo $entry\n")
    outfile.write("ofile=${entry}.flip.fastq\n")
    outfile.write("echo $ofile\n")
    outfile.write("sbatch -J ${ofile}flip --export=infile=$pathandfilename,outfile=$ofile,outdir=$od " + scriptdir + "/flipfastq.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "runflipfastq.sbatch > " + tempdir + "/Job_ID.txt")