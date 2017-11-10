# Map

This package takes as input fastq or SRA files and runs through the Dowell Lab pipeline to convert these files into sorted bams, bedgraphs (normalized to millions mapped) and tdf files (to visualize on a genome browser such as IGV).

This python package is meant to be run on the fiji cluster at the University of Colorado at Boulder.

To access the fiji compute cluster:
ssh identikey@fiji.colorado.edu

There are several modules in this package which can be turned on/off by switching booleans within src/main.py - Before running, please check:

  1. You are running all desired modules (some of these will depend on which sequencing kit you've used/what type of  sequencing data you are looking at)

  2. You are pointing to the correct genome files

To run:
cd Map/
python src/ /full/path/to/SRAorFASTQ/
