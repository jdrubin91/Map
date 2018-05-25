__author__ = 'Jonathan Rubin'
#Scripts adapted from Josephina Hendrix and Mary Allen

#Required modules:
#module load cutadapt/1.2.1
#module load sra/2.8.0
#module load samtools/1.3.1
#module load bedtools2/2.25.0
#Also need to git clone TrimGalore if using trim module into Map/ directory:
#git clone https://github.com/FelixKrueger/TrimGalore.git

import sys
import os
import datetime
import trim_galore
import trimmomatic
import write_scripts
import sra_to_fastq
import check_job
import quality_check
import flip_reads
import fastq_to_sam
import sam_to_bam
import rseqc
import preseq
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

#Specify genome
genome = 'hg19'
# genome = 'dm3'
# genome = 'mm10'
# genome = 'ERCC'

#Specify bowtie options
#Used for ChIP-Seq
# bowtieoptions = "-k 1 -n 2 -l 36 --best"
#Used for GRO-Seq
bowtieoptions = "--very-sensitive"
# bowtieoptions = "-p 4 -S"
#Used for ATAC-Seq
#bowtieoptions = "-X2000"
#Used for RNAPII-ChIP
# bowtieoptions = "-n 1 -m 1-best-strata"

#Trim adaptors?
trimgalore = False
trimmomaticbool = False
#If no options desired use "" else needs a space at the end. This no longer works (JDR 8/22/17).
trimgaloreoptions = ""
# trimgaloreoptions = "--clip_R1 15 "

#Check read quality?
quality=True

#Flip reads? This is used for some GRO-Seq protocols
flip = False

#Check for Spike-In controls? Only True if you added spike-in controls from Jonathan Rubin to your GRO-Seq samples
spike= False

#Booleans for all steps in pipeline (lets you only run part of the pipeline. If using this feature make sure above booleans are set appropriately
#and you specify the correct path to input files. (JDR 8/30/17)
sratofastq = False
fastqtosam = False
samtobam = False
bamtobedgraph = False
readcountcorrection = False
igvcreate = False
millionsmapped = False

#======================================================================

#Return parent directory
def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

#Full path to genome construct and bowtie indexes. Genome files contain two tab separated columns: Chromosome, Length of chromosome.
#Bowtie indexes can be created with bowtie and a fasta file of your genome using the command:
#bowtie2-build genomefasta.fa basename
#genomefasta.fa = fasta file of entire genome
#basename = base filename given to bowtie index files
#If you don't have these files, copy /projects/Down/Dowellseq/genomes/bowtiebwaindexs/ to your scratch directory and specify in 
#index_directory, where you've copied this folder
index_directory = '/scratch/Users/joru1876/bowtiebwaindexes/'
if genome == 'hg19':
    genomedir=index_directory + 'human.hg19.genome'
    bowtieindex=index_directory + 'hg19_Bowtie2_indexp32'
elif genome == 'dm3':
    genomedir=index_directory + 'dm3.fa.genome'
    bowtieindex=index_directory + 'dm3.fa.Bowtie2'
elif genome == 'mm10':
    genomedir=index_directory + 'mm10.genome'
    bowtieindex=index_directory + 'mm10_Bowtie2_index'
elif genome == 'ERCC':
    bowtieindex=index_directory + 'ERCC92_Bowtie2_index'
    genomedir=index_directory + 'ERCC.genome'
else:
    sys.exit("Genome not found, exiting...")

#Path to spike-in control genomes
spikeingenomedir='/scratch/Shares/dowell/bowtie2_indices/JDR_SpikeIn/'
SpikeIngenomes=[spikeingenomedir+'LBS-1.genome',spikeingenomedir+'A-region.genome',spikeingenomedir+'LBS-3.genome',spikeingenomedir+'C-unit.genome',spikeingenomedir+'TRNAS23.genome']

#Path to spike-in control bowtie indexes
spikeinindexdir = '/scratch/Shares/dowell/bowtie2_indices/JDR_SpikeIn/bowtiebwaindexs/'
SpikeInbowtieindexes=[spikeinindexdir+'LBS-1',spikeinindexdir+'A-region',spikeinindexdir+'LBS-3',spikeinindexdir+'C-unit',spikeinindexdir+'TRNAS23']


#Home directory
homedir = os.path.dirname(os.path.realpath(__file__))

#Temporary files directory
tempdir = parent_dir(homedir) + '/temp'

#Full path to 12-bed gene annotations
genefile = parent_dir(homedir) + '/annotations/' + genome + '_annotations.bed'

#Full path to 12-bed rRNA annotations
rRNAfile = parent_dir(homedir) + '/annotations/' + genome + '.rRNA.bed'

#Directory to temporary job file
job = tempdir + "/Job_ID.txt"

#Trim Galore directory
trimgalore = parent_dir(homedir) + '/TrimGalore/'

#Trimmomatic directory
trimmomaticdir = parent_dir(homedir) + '/Trimmomatic-0.36/trimmomatic-0.36.jar'


def run():
    print "Filepath: ", fullpath

    #Creates an ouptut directory in the specified full path to your files
    output = fullpath + datetime.datetime.now().strftime("%Y%m%d") + '_Map-0/'
    if os.path.isdir(output):
        maximum = 0
        for file1 in os.listdir(fullpath):
            if '_Map-' in file1:
                output_number = int(file1.split('_Map-')[-1])
                if output_number > maximum:
                    maximum = output_number
        output = fullpath + datetime.datetime.now().strftime("%Y%m%d") + '_Map-' + str(maximum+1) + '/'
        print "Output Directory: ", output
        os.makedirs(output)
    else:
        print "Output Directory: ", output
        os.makedirs(output)

    print "Initializing Output Subdirectories..."
    scriptdir = output + 'scripts/'
    os.makedirs(scriptdir)
    os.system("scp " + parent_dir(homedir) + '/scripts/* ' + scriptdir)
    e_and_o = output + 'e_and_o/'
    os.makedirs(e_and_o)
    print "done"



    #Writes script files based on genome and bowtie index
    print "Writing script files..."
    write_scripts.run(scriptdir,genomedir,bowtieindex,bowtieoptions,email,e_and_o,fullpath)
    print "done"
    
    if sratofastq:
        #Converts SRA to Fastq format
        print "Converting SRA to Fastq..."
        boolean = sra_to_fastq.run(scriptdir, fullpath, tempdir)
        if boolean:
            check_job.run(job,tempdir)
            print "done"
        else:
            print "No SRA files in filepath"

    #Trim adaptor sequences from fastq files
    if trimgalore:
        print "Using trim galore to trim reads..."
        indir = fullpath
        trimdir = output + 'trimmed/'
        os.makedirs(trimdir)
        trim_galore.run_job(trimgalore, scriptdir, indir, trimdir, tempdir)
        check_job.run(job,tempdir)
        for file1 in os.listdir(trimdir):
            if 'fq' in file1.split('.')[-1]:
                os.system("mv " + trimdir + file1 + " " + trimdir + ".".join(file1.split('.')[:-1]) + ".fastq")
        print "done"
    elif trimmomaticbool:
        print "Using trimmomatic to trim reads..."
        newpath = trimmomatic.run(trimmomaticdir,fullpath)
        print "done"

    
    #Checks read quality
    if quality:
        print "Checking Fastq quality..."
        if trimgalore or trimmomaticbool:
            indir = trimdir
        else:
            indir = fullpath
        fastqcdir = output + 'QC/fastqc/'
        os.makedirs(fastqcdir)
        quality_check.run(scriptdir, indir, fastqcdir, tempdir)
        check_job.run(job,tempdir)
        print "done"
    
    #Flips reads (use for some GRO-Seq protocols)
    if flip:
        if trimgalore or trimmomaticbool:
            indir = trimdir
        else:
            indir = fullpath
        flipdir = output + 'flipped/'
        print "Flipping Reads..."
        flip_reads.run(scriptdir, indir, flipdir, tempdir)
        check_job.run(job,tempdir)
        print "done"
    
    #Checks reads mapped to spike-in control genomes
    if spike:
        print "Checking Spike-in Controls..."
        spikeinpath = output + 'spikeins/'
        spikeinscripts = output + 'spikeins/scripts/'
        if not os.path.exists(spikeinpath):
            os.mkdir(spikeinpath)
        if not os.path.exists(spikeinscripts):
            os.mkdir(spikeinscripts)
        if flip:
            indir = flipdir
        elif trimgalore or trimmomaticbool:
            indir = trimdir
        else:
            indir = fullpath
        for i in range(len(SpikeIngenomes)):
            print "Checking reads mapped to: " + SpikeInbowtieindexes[i].split('/')[-1]
            g = SpikeIngenomes[i]
            b = SpikeInbowtieindexes[i]
            write_scripts.run(spikeinscripts,g,b,bowtieoptions,email,e_and_o,spikeinpath)
            fastq_to_sam.run(spikeinscripts, indir, spikeinpath, tempdir, g, boolean=False)
            check_job.run(job,tempdir)

        spikein_results = dict()
        for file1 in [i for i in os.listdir(spikeinpath) if '.stderr' in i]:
            with open(spikeinpath + file1) as F:
                lines = F.readlines()
                total = ('Total: ', int(lines[0].strip('\n').split()[0]))
                spiked = (file1.split('.')[-3] + ': ', int(lines[3].strip('\n').split()[0]) + int(lines[4].strip('\n').split()[0]))
            key = file1.split('.')[0]
            if key not in spikein_results:
                spikein_results[key] = [total,spiked]
            else:
                spikein_results[key].append(spiked)

        outfile = open(spikeinpath + 'spikeins.txt','w')
        for key in spikein_results:
            outfile.write(key+'\n')
            for spike_count in sorted(spikein_results[key], key=lambda x: x[1], reverse=True):
                outfile.write(spike_count[0] + str(spike_count[1]) + '\n')
            
        outfile.close()

        for file1 in [i for i in os.listdir(spikeinpath) if not '.stderr' in i]:
            if not os.path.isdir(spikeinpath + file1) and 'spikeins.txt' not in file1:
                os.system("rm " + spikeinpath + file1)
        print "done"



    if fastqtosam:
        #Converts Fastq to SAM format
        print "Converting Fastq to SAM..."
        if flip:
            indir = flipdir
        elif trimgalore or trimmomaticbool:
            indir = trimdir
        else:
            indir = fullpath
        samdir = output + 'SAM/'
        newpath = fastq_to_sam.run(scriptdir, indir, samdir, tempdir, genomedir)
        check_job.run(job,tempdir)
        print "done"
    
    if samtobam:
        #Converts SAM to BAM format
        print "Converting SAM to BAM..."
        if fastqtosam:
            indir = samdir
        else:
            indir = fullpath
        bamdir = output + 'BAM/'
        sam_to_bam.run(scriptdir, indir, bamdir, tempdir)
        check_job.run(job,tempdir)
        print "done"

    if quality:
        print "Checking BAM quality..."
        if samtobam:
            indir = bamdir
        else:
            indir = fullpath
        rseqcdir = output + 'QC/rseqc/'
        preseqdir = output + 'QC/preseq/'
        os.makedirs(rseqcdir)
        os.makedirs(preseqdir)
        print "Running preseq..."
        preseq.run(scriptdir, indir, preseqdir, tempdir)
        check_job.run(job,tempdir)
        print "done\nRunning rseqc..."
        rseqc.run(scriptdir, indir, rseqcdir, genefile, rRNAfile, tempdir)
        check_job.run(job,tempdir)
        rseqc.compile_results(rseqcdir)

        print "done"
    
    if bamtobedgraph:
        #Converts BAM to Bedgraph format
        print "Converting BAM to Bedgraph..."
        if samtobam:
            indir = bamdir
        else:
            indir = fullpath
        bedgraphdir = output
        bam_to_bedgraph.run(scriptdir, indir, bedgraphdir, tempdir)
        check_job.run(job,tempdir)
        print "done"
    
    if readcountcorrection:
        #Normalizes bedgraphs to millions mapped
        print "Correcting for readcounts..."
        if samtobam:
            indir = bamdir
        else:
            indir = fullpath
        outdir = output + 'TDF/'
        readcount_correction.run(scriptdir, indir, outdir)
        print "done"
    
    if igvcreate:
        #Creates IGV scripts 
        print "Creating IGV files..."
        if bamtobedgraph:
            indir = output + 'TDF/'
        else:
            indir = output
        igv_create.run(scriptdir, indir, tempdir, genome, e_and_o, email)
        check_job.run(job,tempdir)
        print "done"
    
    if millions_mapped:
        print "Getting millions mapped reads..."
        if samtobam:
            indir = bamdir
        else:
            indir = fullpath
        millions_mapped.run(scriptdir, indir)
        print "done"
    
    
    
    
