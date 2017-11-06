#PBS -V
#PBS -q longmem
#PBS -l walltime=96:00:00
#PBS -l nodes=1:ppn=1
### Use the bourne shell
#PBS -S /bin/sh

### Set your email address
#PBS -m ae
#PBS -M joru1876@colorado.edu




/opt/fastx/0.0.13.2/bin/fastx_reverse_complement -Q33 -i $infile -o ${outdir}${outfile}
wc1=`wc -l $infile | awk '{print $1}'`
wc2=`wc -l ${outdir}${outfile} | awk '{print $1}'`
if [ $wc1 -ne $wc2 ]
then
echo "error lines don't match" 
echo $infile
echo $wc1 
echo ${outdir}${outfile}
echo $wc2
fi
