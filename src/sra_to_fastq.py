__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    boolean = False
    for file1 in os.listdir(fullpath):
        if 'sra' in file1:
            boolean = True
    if boolean:
        output = fullpath + 'fastq/'
        if not os.path.isdir(output):
            os.makedirs(output)
        outfile = open(scriptdir + '/runsradump.sh', 'w')
        outfile.write("indir=" + output + "\n")
        outfile.write("od=" + output + "\n")
        outfile.write("for pathandfilename in `ls $indir*.sra`; do\n")
        outfile.write("entry=`basename $pathandfilename .sra`\n")
        outfile.write("infilename=$pathandfilename\n")
        outfile.write("sbatch -J sradump${entry} --export=infile=$infilename,outdir=$od " + scriptdir + "/sradump.sbatch\n")
        outfile.write("done")
        outfile.close()
        
        os.system("bash " + scriptdir + "/runsradump.sh > " + tempdir + "/Job_ID.txt")
    
    return boolean