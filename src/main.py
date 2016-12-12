__author__ = 'Jonathan Rubin'
#Scripts adapted from Josephina Hendrix and Mary Allen

#Required modules: 
#module load sra_2.3.2-5
#module load samtools_0.1.19
#module load bedtools2_2.22.0

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
#Give full path to SRA files or FASTQ files (remember to include a '/' at the end)
fullpath = sys.argv[1]

#Give email address where job e-mails will be sent
email="joru1876@colorado.edu"

#Give full path to desired genome construct. Genome files contain two tab separated columns: Chromosome, Length of chromosome
genome='/projects/dowellLab/groseq/forJoey/human.hg19.genome'
#genome='/projects/dowellLab/groseq/forJoey/dro/dm3.fa.genome'
#genome='/projects/dowellLab/groseq/forJoey/mm10.genome'

#Path to spike-in control genomes
SpikeIngenomes=['/projects/Down/Dowellseq/genomes/LBS-1.genome','/projects/Down/Dowellseq/genomes/A-region.genome','/projects/Down/Dowellseq/genomes/LBS-3.genome','/projects/Down/Dowellseq/genomes/C-unit.genome','/projects/Down/Dowellseq/genomes/TRNAS23.genome']

#Give full path to bowtie indexes, these can be created with bowtie and a fasta file of your genome using the command:
#bowtie2-build genomefasta.fa basename
#genomefasta.fa = fasta file of entire genome
#basename = base filename given to bowtie index files
#Give full path to bowtie indexes with basename at end

bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/hg19_Bowtie2_indexp32'
#bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/mm10_Bowtie2_index'
#bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/dm3.fa.Bowtie2'
#bowtieindex='/projects/Down/Dowellseq/genomes/bowtiebwaindexs/ERCC92_Bowtie2_index'

#Path to spike-in control bowtie indexes
SpikeInbowtieindexes=['/projects/Down/Dowellseq/genomes/bowtiebwaindexs/LBS-1','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/A-region','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/LBS-3','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/C-unit','/projects/Down/Dowellseq/genomes/bowtiebwaindexs/TRNAS23']


#Specify bowtie options
#Used for ChIP-Seq
# bowtieoptions = "-k 1 -n 2 -l 36 --best"
#Used for GRO-Seq
#bowtieoptions = "--very-sensitive"
#Used for ATAC-Seq
#bowtieoptions = "-X2000"
#Used for RNAPII-ChIP
bowtieoptions = "-n 1 -m 1-best-strata"

#Check read quality?
quality=True

#Flip reads? This is used for some GRO-Seq protocols
flip = False

#Check for Spike-In controls? Only True if you added spike-in controls from Jonathan Rubin to your GRO-Seq samples
spike= False
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
    if quality:
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
    
    #Checks reads mapped to spike-in control genomes
    if spike:
        print "done\nChecking Spike-in Controls..."
        if not os.path.exists(newpath + 'bowtie2/'):
            os.mkdir(newpath + 'bowtie2/')
        if not os.path.exists(newpath + 'bowtie2/spikeins/'):
            os.mkdir(newpath + 'bowtie2/spikeins/')
        for i in range(len(SpikeIngenomes)):
            print "Checking reads mapped to: " + SpikeInbowtieindexes[i].split('/')[-1]
            g = SpikeIngenomes[i]
            b = SpikeInbowtieindexes[i]
            write_scripts.run(scriptdir,g,b,bowtieoptions)
            fastq_to_sam.run(scriptdir, newpath, tempdir, g, boolean=False)
            check_job.run(job,tempdir)
        for file1 in [i for i in os.listdir(newpath + 'bowtie2/spikeins/') if '.stderr' in i]:
            print file1.split('.')[0] + file1.split('.')[2]
            with open(newpath + 'bowtie2/spikeins/' + file1) as F:
                for line in F:
                    print line



    #Writes script files based on genome and bowtie index
    print "done\nWriting script files..."
    write_scripts.run(scriptdir,genome,bowtieindex,bowtieoptions,email)

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
    
    
    
    