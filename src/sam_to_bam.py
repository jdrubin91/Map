__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, indir, bamdir, tempdir):
    outfile = open(scriptdir + 'runsamtobaidir.sbatch', 'w')
    outfile.write("id=" + indir + "\n")
    outfile.write("od=" + bamdir + "\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $id*.sam`; do\n")
    outfile.write("entry=`basename $pathandfilename .sam`\n")
    outfile.write("echo $entry\n")
    outfile.write("sbatch -J ${entry}samtobai --export=outdir=$od,indir=$id,basename=$entry " + scriptdir + "/samtobai.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "runsamtobaidir.sbatch > " + tempdir + "/Job_ID.txt")