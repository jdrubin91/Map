__author__ = 'Jonathan Rubin'

#Required modules: 
#module load sra_2.3.2-5
#module load samtools_0.1.19

import os
import sra_to_fastq
import check_job
import quality_check
import flip_reads
import fastq_to_sam
import sam_to_bam
import bam_to_bedgraph
import readcount_correction
import igv_create
import millions_mapped


#User-defined input
#======================================================================
#Give full path to SRA files (remember to include a '/' at the end)
fullpath = '/scratch/Users/joru1876/test/'

#Give user ID
user = 'joru1876'
#======================================================================


#Return parent directory
def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

#Home directory
homedir = os.path.dirname(os.path.realpath(__file__))

#Scripts directory
scriptdir = parent_dir(homedir) + '/scripts'

#Temporary files directory
tempdir = parent_dir(homedir) + '/temp'


def run():
    print "SRA filepath: ", fullpath
    #print "Converting SRA to Fastq..."
    #job = sra_to_fastq.run(scriptdir, fullpath, tempdir)
    #check_job.run(job,tempdir)
    print "done\nChecking quality..."
    quality_check.run(scriptdir, fullpath, tempdir)
    #check_job.run(tempdir,user)
    #print "done\nFlipping Reads..."
    #flip_reads.run(scriptdir, fullpath, tempdir)
    #check_job.run(tempdir,user)
    #print "done\nConverting Fastq to SAM..."
    #fastq_to_sam.run(scriptdir, fullpath, tempdir)
    #check_job.run(tempdir,user)
    #print "done\nConverting SAM to BAM..."
    #sam_to_bam.run(scriptdir, fullpath, tempdir)
    #check_job.run(tempdir,user)
    #print "done\nConverting BAM to Bedgraph..."
    #bam_to_bedgraph.run(scriptdir, fullpath, tempdir)
    #check_job.run(tempdir,user)
    #print "done\nCorrecting for readcounts..."
    #readcount_correction.run(scriptdir, fullpath)
    #print "done\nCreating IGV files..."
    #igv_create.run(scriptdir, fullpath)
    #print "done\nGetting millions mapped reads..."
    #millions_mapped.run(scriptdir, fullpath)
    #print "done"
    
    
    
    