__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, fullpath, tempdir):
    outfile = open(scriptdir + '/runsamtobaidir.sh', 'w')
    outfile.write("id=" + fullpath + "flipped/bowtie2/")
    outfile.write("od=" + fullpath + "flipped/bowtie2/sortedbam/")
    outfile.write("mkdir -p $od")
    outfile.write("for pathandfilename in `ls $id*.sam`; do")
    outfile.write("entry=`basename $pathandfilename .sam`")
    outfile.write("echo $entry")
    outfile.write("qsub -v outdir=$od,indir=$id,basename=$entry -N ${entry}samtobai " + scriptdir + "/samtobai.sh")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runsamtobaidir.sh > " + tempdir + "/Job_ID.txt")
    
    return tempdir + "/Job_ID.txt"