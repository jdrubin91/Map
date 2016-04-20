
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

genome=/projects/dowellLab/groseq/forJoey/human.hg19.genome
#genome=/projects/dowellLab/groseq/forJoey/dro/dm3.fa.genome
#genome=/projects/dowellLab/groseq/forJoey/mm10.genome

echo $infile
echo $genome
echo $outfile1

mkdir -p  $outdir/genomecoveragebed
mkdir -p $outdir/forFstitch
mkdir -p $outdir/genomecoveragebed/fortdf

/opt/bedtools/2.22.0/genomeCoverageBed -5 -bg -strand + -ibam $infile -g $genome > $outdir/forFstitch/$outfile1
/opt/bedtools/2.22.0/genomeCoverageBed -5 -bg -strand - -ibam $infile -g $genome > $outdir/forFstitch/$outfile2
/opt/bedtools/2.22.0/genomeCoverageBed -bg -strand + -ibam $infile -g $genome > $outdir/genomecoveragebed/$outfile3
/opt/bedtools/2.22.0/genomeCoverageBed -bg -strand - -ibam $infile -g $genome | awk -F '\t' -v OFS='\t' '{ $4 = - $4 ; print $0 }'> $outdir/genomecoveragebed/$outfile4
cat $outdir/genomecoveragebed/$outfile4 $outdir/genomecoveragebed/$outfile3 > $outdir/genomecoveragebed/fortdf/$outfile5.bed
/opt/bedtools/2.22.0/sortBed -i $outdir/genomecoveragebed/fortdf/$outfile5.bed >$outdir/genomecoveragebed/fortdf/$outfile5

