__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runbam_to_5primebed.sh', 'w')
    outfile.write("indir=" + fullpath + "flipped/bowtie2/sortedbam/\n")
    outfile.write("odir=" + fullpath + "flipped/bowtie2/sortedbam/\n")
    outfile.write("for pathandfilename in `ls $indir*.bam`; do\n")
    outfile.write("entry=`basename $pathandfilename .bam`\n")
    outfile.write("infilename=$pathandfilename\n")
    outfile.write("otfile1=${entry}.fiveprime.pos.BedGraph\n")
    outfile.write("otfile2=${entry}.fiveprime.neg.BedGraph\n")
    outfile.write("otfile3=${entry}.pos.BedGraph\n")
    outfile.write("otfile4=${entry}.neg.BedGraph\n")
    outfile.write("otfile5=${entry}.BedGraph\n")
    outfile.write("bed=${entry}.bed\n")
    outfile.write("fiveprime=${entry}.fiveprime.bed\n")
    outfile.write("qsub -v infile=$infilename,bedfile=$bed,fivebrimebedfile=$fiveprime,outdir=$odir,outfile1=$otfile1,outfile2=$otfile2,outfile3=$otfile3,outfile4=$otfile4,outfile5=$otfile5 -N ${entry}BEDgrAPH " + scriptdir + "/bam_to_5primebed.sh\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runbam_to_5primebed.sh > " + tempdir + "/Job_ID.txt")
    
    return tempdir + "/Job_ID.txt"