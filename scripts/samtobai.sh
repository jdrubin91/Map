
#PBS -q longmem 
#PBS -V
#PBS -l pmem=100gb
#PBS -l walltime=96:00:00
#PBS -lnodes=1:ppn=1
### Use the bourne shell
#PBS -S /bin/sh

### Set your email address
#PBS -m ae
#PBS -M joru1876@colorado.edu

cd $PBS_O_WORKDIR
echo Working directory is $PBS_O_WORKDIR
mkdir -p $outdir

#wc -l ${indir}${basename}.sam > ${outdir}${basename}.sam.wc
samtools view -S -b -o ${outdir}${basename}.bam ${indir}${basename}.sam 2>${outdir}${basename}.bam.err
samtools sort -m100000000000 ${outdir}${basename}.bam ${outdir}${basename}.sorted
samtools flagstat ${outdir}${basename}.bam > ${outdir}${basename}.bam.flagstat 2>${outdir}${basename}.bam.flagstat.err
samtools index ${outdir}${basename}.sorted.bam
samtools flagstat ${outdir}${basename}.sorted.bam > ${outdir}${basename}.sorted.bam.flagstat 2>${outdir}${basename}.sorted.bam.flagstat.err



