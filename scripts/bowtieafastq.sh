#PBS -q long2gb

### Use the bourne shell
#PBS -S /bin/sh

### Specify the number of nodes and processors for your job
#PBS -l nodes=1:ppn=32


#PBS -m ae
#PBS -o /scratch/Users/joru1876/qsub_stdo/
#PBS -e /scratch/Users/joru1876/qsub_errors/

### Switch to the working directory; by default TORQUE launches processes
### from your home directory.  This is a good idea because your -o and -e files 
### will go here
cd $PBS_O_WORKDIR
echo Working directory is $PBS_O_WORKDIR

### Retrieve/use all modules loaded ###
#PBS -V

echo $fastq1pathandfile
echo ${outdir}${outfile}.sam 

###bowtie2 -pNumberOfProcessors <indexedGenome.prefix> -q <input.fastq> -S <output.sam> 2> <output.stderr>
/opt/bowtie/bowtie2-2.0.2/bowtie2 -p32 --very-sensitive \
/projects/Down/Dowellseq/genomes/bowtiebwaindexs/hg19_Bowtie2_indexp32 \
-U $fastq1pathandfile \
> ${outdir}${outfile}.sam \
2> ${outdir}${outfile}.stderr
###/projects/Down/Dowellseq/genomes/bowtiebwaindexs/mm10_Bowtie2_index\
###/projects/Down/Dowellseq/genomes/bowtiebwaindexs/dm3.fa.Bowtie2\
###-U $fastq1pathandfile \
###> ${outdir}${outfile}.sam \
###2> ${outdir}${outfile}.stderr




