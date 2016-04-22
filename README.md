# Map

This package requires the following modules:\n
module load sra_2.3.2-5\n
module load samtools_0.1.19\n

Additionally, this package requires that you have access to /projects on the compute cluster in CU Boulder
If this is not the case, bowtie index path must be changed in Map/scripts/bowtieafastq.sh and genome path must be changed in Map/scripts/bam_to_5primebed.sh

To run:
1. Go into Map/
2. python src/ <full/path/to/SRA/> ('/' at the end of path is necessary)

This package will check whether jobs have been completed every 10 seconds.  This can be changed in Map/src/check_job.py.

Parts of main.py can be commented out depending on which mapping steps you would like to run.  As it is written, part of the mapping procedure will flip your initial reads (which is necessary for some protocols).  This step is necessary right now as a 'flipped' directory has been hard coded into the script. You can fix this by going into the scripts after Map/src/flip_reads.py and altering the paths to not include the 'flipped' directory.
