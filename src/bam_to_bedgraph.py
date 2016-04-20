__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runbam_to_5primebed.sh', 'w')
    outfile.write("indir=" + fullpath + "flipped/bowtie2/sortedbam/")
    outfile.write("odir=" + fullpath + "flipped/bowtie2/sortedbam/")
    outfile.write("for pathandfilename in `ls $indir*.bam`; do")
    outfile.write("entry=`basename $pathandfilename .bam`")
    outfile.write("infilename=$pathandfilename")
    outfile.write("otfile1=${entry}.fiveprime.pos.BedGraph")
    outfile.write("otfile2=${entry}.fiveprime.neg.BedGraph")
    outfile.write("otfile3=${entry}.pos.BedGraph")
    outfile.write("otfile4=${entry}.neg.BedGraph")
    outfile.write("otfile5=${entry}.BedGraph")
    outfile.write("bed=${entry}.bed")
    outfile.write("fiveprime=${entry}.fiveprime.bed")
    outfile.write("qsub -v infile=$infilename,bedfile=$bed,fivebrimebedfile=$fiveprime,outdir=$odir,outfile1=$otfile1,outfile2=$otfile2,outfile3=$otfile3,outfile4=$otfile4,outfile5=$otfile5 -N ${entry}BEDgrAPH " + scriptdir + "/bam_to_5primebed.sh")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runbam_to_5primebed.sh > " + tempdir + "/Job_ID.txt")
    
    return tempdir + "/Job_ID.txt"