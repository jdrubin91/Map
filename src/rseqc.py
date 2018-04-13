__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, rseqcdir, genefile, rRNAfile, tempdir):
    outfile = open(scriptdir + 'run_rseqc.sbatch', 'w')
    outfile.write("indir=" + indir + "\n")
    outfile.write("odir=" + rseqcdir + "\n")
    outfile.write("for pathandfilename in `ls $indir*.sorted.bam`; do\n")
    outfile.write("entry=`basename $pathandfilename`\n")
    outfile.write("outfile=${odir}${entry}\n")
    outfile.write("infilename=$pathandfilename\n")
    outfile.write("bed="+genefile+"\n")
    outfile.write("bed2="+rRNAfile+"\n")
    outfile.write("sbatch -J ${entry}rseqc --export=infile=$infilename,genefile=$bed,rRNAfile=$bed2,ofile=$outfile " + scriptdir + "/rseqc.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "run_rseqc.sbatch > " + tempdir + "/Job_ID.txt")

def compile_results(rseqcdir):
    filenames = list()
    for file1 in os.listdir(rseqcdir):
        filename = file1.split('sorted.bam')[0]
        if filename not in filenames:
            filenames.append(filename)

    for filename in filenames:
        fullfilename = rseqcdir + filename + 'sorted.bam'
        outfile = open(fullfilename+'.rseqc_results.txt','w')
        outfile.write("""=============
|bam_stat.py|
=============\n\n""")
        with open(fullfilename+'.bam_stat.txt') as F:
            for line in F:
                outfile.write(line)
        outfile.write("""\n\n======================
|read_distribution.py|
======================\n\n""")
        with open(fullfilename+'.read_distribution.txt') as F:
            for line in F:
                outfile.write(line)
        outfile.write("""\n\n=====================
|rRNA (split_bam.py)|
=====================\n\n""")
        outfile.write("=========================\nReads mapped to rRNA\n")
        with open(fullfilename+'.in.bam.flagstat') as F:
            lines = F.readlines()
            outfile.write(lines[0])
        outfile.write("=========================\nReads NOT mapped to rRNA\n")
        with open(fullfilename+'.ex.bam.flagstat') as F:
            lines = F.readlines()
            outfile.write(lines[0])
        outfile.write("=========================\nUnmapped reads\n")
        with open(fullfilename+'.junk.bam.flagstat') as F:
            lines = F.readlines()
            outfile.write(lines[0])
        outfile.write("""\n\n=====================
|read_duplication.py|
=====================\n\n""")
        outfile.write("Sequence based: reads with identical sequence are regarded as duplicated reads.\n")
        column1 = list()
        column2 = list()
        with open(fullfilename+'.seq.DupRate.xls') as F:
            for line in F:
                val1,val2 = line.strip('\n').split()
                column1.append(val1)
                column2.append(val2)
        outfile.write('\t'.join(column1)+'\n')
        outfile.write('\t'.join(column2)+'\n')
        outfile.write("\nMapping based: reads mapped to the exactly same genomic location are regarded as duplicated reads.\n")
        column1 = list()
        column2 = list()
        with open(fullfilename+'.pos.DupRate.xls') as F:
            for line in F:
                val1,val2 = line.strip('\n').split()
                column1.append(val1)
                column2.append(val2)
        outfile.write('\t'.join(column1)+'\n')
        outfile.write('\t'.join(column2)+'\n')
        outfile.close()
    for file1 in os.listdir(rseqcdir):
        if '.rseqc_results.txt' not in file1:
            os.system("rm " + rseqcdir + file1)