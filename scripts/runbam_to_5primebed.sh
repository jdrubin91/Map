indir=/projects/dowellLab/Taatjes/170825_NB501447_0152_fastq/Demux/cat/trimmed/flipped/bowtie2/sortedbam/
odir=/projects/dowellLab/Taatjes/170825_NB501447_0152_fastq/Demux/cat/trimmed/flipped/bowtie2/sortedbam/
for pathandfilename in `ls $indir*.sorted.bam`; do
entry=`basename $pathandfilename .bam`
infilename=$pathandfilename
otfile1=${entry}.fiveprime.pos.BedGraph
otfile2=${entry}.fiveprime.neg.BedGraph
otfile3=${entry}.pos.BedGraph
otfile4=${entry}.neg.BedGraph
otfile5=${entry}.BedGraph
bed=${entry}.bed
fiveprime=${entry}.fiveprime.bed
qsub -v infile=$infilename,bedfile=$bed,fivebrimebedfile=$fiveprime,outdir=$odir,outfile1=$otfile1,outfile2=$otfile2,outfile3=$otfile3,outfile4=$otfile4,outfile5=$otfile5 -N ${entry}BEDgrAPH /Users/jonathanrubin/Google Drive/Colorado University/Jonathan/Map/scripts/bam_to_5primebed.sh
done