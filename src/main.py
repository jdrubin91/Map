__author__ = 'Jonathan Rubin'
#Scripts adapted from Josephina Hendrix and Mary Allen

#Required modules: 
#module load sra_2.3.2-5
#module load samtools_0.1.19

import sys
import os
import write_scripts
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
fullpath = sys.argv[1]

#Give full path to desired genome construct
genome='/projects/dowellLab/groseq/forJoey/human.hg19.genome'
#genome='/projects/dowellLab/groseq/forJoey/dro/dm3.fa.genome'
#genome='/projects/dowellLab/groseq/forJoey/mm10.genome'

#Path to spike-in control genomes
SpikeIngenomes=['/projects/Down/Dowellseq/genomes/LBS-1.genome','/projects/Down/Dowellseq/genomes/A-region.genome','/projects/Down/Dowellseq/genomes/LBS-3.genome','/projects/Down/Dowellseq/genomes/C-unit.genome']


#Give full path to bowtie indexes, these can be created with bowtie and a fasta file of your genome
bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/hg19_Bowtie2_indexp32'
#bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/mm10_Bowtie2_index'
#bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/dm3.fa.Bowtie2'
#bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/ERCC92_Bowtie2_index'

#Path to spike-in control bowtie indexes
SpikeInbowtieindexes=['/projects/Down/Dowellseq/genomes/bowtiebwaindexs/LBS-1','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/A-region','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/LBS-3','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/C-unit']


#Specify bowtie options
# bowtieoptions = "-p32 -k 1 -n 2 -l 36 --best"
bowtieoptions = "-p32 --very-sensitive"

#Flip reads? This is used for some GRO-Seq protocols
flip = False

#Check for Spike-In controls? Only True if you added spike-in controls from Jonathan Rubin to your GRO-Seq samples
spike= True
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

#Directory to temporary job file
job = tempdir + "/Job_ID.txt"


def run():
    print "Filepath: ", fullpath
    
    #Converts SRA to Fastq format
    print "Converting SRA to Fastq..."
    boolean = sra_to_fastq.run(scriptdir, fullpath, tempdir)
    if boolean:
        check_job.run(job,tempdir)
        print "done"
    else:
        print "No SRA files in filepath"
    
    #Checks read quality
    print "done\nChecking quality..."
    quality_check.run(scriptdir, fullpath, tempdir)
    check_job.run(job,tempdir)
    
    #Flips reads (use for some GRO-Seq protocols)
    if flip:
        print "done\nFlipping Reads..."
        newpath = flip_reads.run(scriptdir, fullpath, tempdir)
        check_job.run(job,tempdir)
    else:
        newpath = fullpath
    
    if spike:
        print "done\nChecking Spike-in Controls..."
        for i in range(len(SpikeIngenomes)):
            print "Checking reads mapped to: " + SpikeInbowtieindexes[i].split('/')[-1]
            g = SpikeIngenomes[i]
            b = SpikeInbowtieindexes[i]
            write_scripts.run(scriptdir,g,b,bowtieoptions)
            fastq_to_sam.run(scriptdir, newpath, tempdir,g,boolean=False)
            check_job.run(job,tempdir)



    #Writes script files based on genome and bowtie index
    print "done\nWriting script files..."
    write_scripts.run(scriptdir,genome,bowtieindex,bowtieoptions)

    #Converts Fastq to SAM format
    print "done\nConverting Fastq to SAM..."
    newpath = fastq_to_sam.run(scriptdir, newpath, tempdir, genome)
    check_job.run(job,tempdir)
    
    #Converts SAM to BAM format
    print "done\nConverting SAM to BAM..."
    newpath = sam_to_bam.run(scriptdir, newpath, tempdir)
    check_job.run(job,tempdir)
    
    #Converts BAM to Bedgraph format
    print "done\nConverting BAM to Bedgraph..."
    bam_to_bedgraph.run(scriptdir, newpath, tempdir)
    check_job.run(job,tempdir)
    
    #Normalizes bedgraphs to millions mapped
    print "done\nCorrecting for readcounts..."
    readcount_correction.run(scriptdir, newpath)
    
    #Creates IGV scripts 
    print "done\nCreating IGV files..."
    igv_create.run(scriptdir, newpath)
    
    
    print "done\nGetting millions mapped reads..."
    millions_mapped.run(scriptdir, fullpath)
    
    print "done"
    
    
    
    