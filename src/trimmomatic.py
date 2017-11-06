__author__ = 'Jonathan Rubin'

import os

def run(trimmomaticdir,newpath):
    output = newpath + 'trimmed/'
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            # os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1 + " ILLUMINACLIP:Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 CROP:100 HEADCROP:50")
            # os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1 + " MINLEN:36 CROP:100 HEADCROP:50")
            os.system("java -jar " + trimmomaticdir + " SE " + newpath + file1 + " " + output + file1 + " MINLEN:36 CROP:50")

    return output

def run_job(trimdir, scriptdir, newpath, tempdir):
    outfile = open(scriptdir + '/runtrimmomatic.sbatch', 'w')
    outfile.write("od=" + newpath + "trimmed/\n")
    outfile.write("indir=" + newpath + "\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename .fastq`\n")
    outfile.write("echo $entry\n")
    outfile.write("sbatch -v infile=$pathandfilename,outdir=$od${entry}.trimmed.fastq -N ${entry}_trim " + scriptdir + "/trimmomatic.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runtrimmomatic.sbatch > " + tempdir + "/Job_ID.txt")
    
    return newpath + 'trimmed/'