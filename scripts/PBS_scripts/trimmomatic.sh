#PBS -q long8gb
#PBS -S /bin/sh
#PBS -l nodes=1:ppn=1
#PBS -e /projects/dowellLab/groseq/pubgro/o_and_e/
#PBS -o /projects/dowellLab/groseq/pubgro/o_and_e/

### Set your email address
#PBS -m ae
#PBS -M joru1876@colorado.edu

### Switch to the working directory; by default TORQUE launches processes
### from your home directory.  This is a good idea because your -o and -e files 
### will go here
cd $PBS_O_WORKDIR
echo Working directory is $PBS_O_WORKDIR

### Retrieve/use all modules loaded ###
#PBS -V


java -XX:ParallelGCThreads=1 -jar /opt/trimmomatic/0.32/trimmomatic-0.32.jar SE $infile $outdir ILLUMINACLIP:Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10
