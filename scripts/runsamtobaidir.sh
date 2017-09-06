id=/projects/dowellLab/Taatjes/170825_NB501447_0152_fastq/Demux/cat/trimmed/flipped/bowtie2/
od=/projects/dowellLab/Taatjes/170825_NB501447_0152_fastq/Demux/cat/trimmed/flipped/bowtie2/sortedbam/
mkdir -p $od
for pathandfilename in `ls $id*.sam`; do
entry=`basename $pathandfilename .sam`
echo $entry
qsub -v outdir=$od,indir=$id,basename=$entry -N ${entry}samtobai /Users/jonathanrubin/Google Drive/Colorado University/Jonathan/Map/scripts/samtobai.sh
done