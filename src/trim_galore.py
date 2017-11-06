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

def run_job(trimdir, scriptdir, newpath, tempdir):
    outfile = open(scriptdir + '/runtrimgalore.sbatch', 'w')
    outfile.write("od=" + newpath + "trimmed/\n")
    outfile.write("indir=" + newpath + "\n")
    outfile.write("mkdir -p $od\n")
    outfile.write("for pathandfilename in `ls $indir*.fastq`; do\n")
    outfile.write("entry=`basename $pathandfilename .fastq`\n")
    outfile.write("echo $entry\n")
    outfile.write("sbatch -J ${entry}_trim --export=trimdir=" + trimdir + ",infile=$pathandfilename,outdir=$od " + scriptdir + "/trim_galore.sbatch\n")
    outfile.write("done")
    outfile.close()
    
    os.system("bash " + scriptdir + "/runtrimgalore.sbatch > " + tempdir + "/Job_ID.txt")
    
    return newpath + 'trimmed/'
