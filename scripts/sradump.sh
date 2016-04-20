
### Run in desired queue
#PBS -q long8gb

### Use the bourne shell
#PBS -S /bin/sh

### Specify the number of nodes and processors for your job
#PBS -l nodes=1:ppn=1

#PBS -m ae
#PBS -o /projects/dowellLab/groseq/pubgro/e_and_o/
#PBS -e /projects/dowellLab/groseq/pubgro/e_and_o/

### Switch to the working directory; by default TORQUE launches processes
### from your home directory.  This is a good idea because your -o and -e files 
### will go here
cd $PBS_O_WORKDIR
echo Working directory is $PBS_O_WORKDIR

### Retrieve/use all modules loaded ###
#PBS -V

### fastq-dump $infile
/opt/sra/2.3.2-5/bin/fastq-dump $infile

