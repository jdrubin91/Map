__author__ = 'Jonathan Rubin'

import os

def run(trimdir,trimoptions,newpath):
    output = newpath + 'trimmed/'
    os.system("mkdir " + output)
    for file1 in os.listdir(newpath):
        if 'fastq' in file1.split('.')[-1]:
            os.system(trimdir + "trim_galore -o " + output + " " + trimoptions + newpath + file1)
    for file1 in os.listdir(output):
        if 'fq' in file1.split('.')[-1]:
            os.system("mv " + output + file1 + " " + output + ".".join(file1.split('.')[:-1]) + ".fastq")

    return output

def run_job(trimgalore, scriptdir, indir ,trimdir, tempdir):
    outfile = open(scriptdir + 'runtrimgalore.sbatch', 'w')
    outfile.write("od=" + trimdir + "\n")
    outfile.write("indir=" + indir + "\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename .fastq`\n")
    outfile.write("echo $entry\n")
    outfile.write("sbatch -J ${entry}_trim --export=trimdir=" + trimgalore + ",infile=$pathandfilename,outdir=$od " + scriptdir + "/trim_galore.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "runtrimgalore.sbatch > " + tempdir + "/Job_ID.txt")

