__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, newpath, tempdir):
    outfile = open(scriptdir + '/runbam_to_5primebed.sbatch', 'w')
    outfile.write("indir=" + newpath + "\n")
    outfile.write("odir=" + newpath + "\n")
    outfile.write("for pathandfilename in `ls $indir*.sorted.bam`; do\n")
    outfile.write("entry=`basename $pathandfilename .bam`\n")
    outfile.write("infilename=$pathandfilename\n")
    outfile.write("otfile1=${entry}.fiveprime.pos.BedGraph\n")
    outfile.write("otfile2=${entry}.fiveprime.neg.BedGraph\n")
    outfile.write("otfile3=${entry}.pos.BedGraph\n")
    outfile.write("otfile4=${entry}.neg.BedGraph\n")
    outfile.write("otfile5=${entry}.BedGraph\n")
    outfile.write("bed=${entry}.bed\n")
    outfile.write("fiveprime=${entry}.fiveprime.bed\n")
    outfile.write("sbatch -J ${entry}BamtoBegraph --export=infile=$infilename,bedfile=$bed,fivebrimebedfile=$fiveprime,outdir=$odir,outfile1=$otfile1,outfile2=$otfile2,outfile3=$otfile3,outfile4=$otfile4,outfile5=$otfile5 " + scriptdir + "/bam_to_5primebed.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runbam_to_5primebed.sbatch > " + tempdir + "/Job_ID.txt")