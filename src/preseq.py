__author__ = 'Jonathan Rubin'

def run(scriptdir, indir, rseqcdir, genefile, rRNAfile, tempdir):
    outfile = open(scriptdir + 'run_preseq.sbatch', 'w')
    outfile.write("indir=" + indir + "\n")
    outfile.write("odir=" + rseqcdir + "\n")
    outfile.write("for pathandfilename in `ls $indir*.sorted.bam`; do\n")
    outfile.write("entry=`basename $pathandfilename`\n")
    outfile.write("outfile=${odir}${entry}\n")
    outfile.write("infilename=$pathandfilename\n")
    outfile.write("sbatch -J ${entry}preseq --export=infile=$infilename,ofile=$outfile " + scriptdir + "/preseq.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "run_preseq.sbatch > " + tempdir + "/Job_ID.txt")