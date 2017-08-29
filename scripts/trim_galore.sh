#PBS -q long8gb
#PBS -S /bin/sh
#PBS -l nodes=1:ppn=1
#PBS -e /Users/joru1876/qsub_errors
#PBS -o /Users/joru1876/qsub_stdo

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


${trimdir}trim_galore -o $outdir $infile
