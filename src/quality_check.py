__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, qualitydir, tempdir):
    outfile = open(scriptdir + '/runqual.sbatch', 'w')
    outfile.write("id=" + indir + "\n")
    outfile.write("od=" + qualitydir + "\n")
    outfile.write("for pathandfilename in `ls $id*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename`\n")
    outfile.write("sbatch -J ${entry}_qual --export=filename=$entry,indir=$id,outdir=$od " + scriptdir + "/qual.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runqual.sbatch > " + tempdir + "/Job_ID.txt")