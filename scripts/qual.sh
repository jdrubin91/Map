#PBS -q longmem
#PBS -S /bin/sh
#PBS -l nodes=1:ppn=1
#PBS -e /projects/dowellLab/groseq/pubgro/o_and_e/
#PBS -o /projects/dowellLab/groseq/pubgro/o_and_e/
#PBS -m ae

### Switch to the working directory; by default TORQUE launches processes
### from your home directory.  This is a good idea because your -o and -e files 
### will go here
cd $PBS_O_WORKDIR
echo Working directory is $PBS_O_WORKDIR

### Retrieve/use all modules loaded ###
#PBS -V

echo $indir${filename}
echo $outdir${filename}.stats


/opt/FastQC/fastqc $indir${filename}


#/opt/fastx/0.0.13.2/bin/fastx_quality_stats -Q33 -i $indir${filename} -o $outdir${filename}.stats >$outdir${filename}.stats.out 2>$outdir${filename}.stats.err 

#echo "done with stats"

#/opt/fastx/0.0.13.2/bin/fastx_nucleotide_distribution_graph.sh -t $outdir${filename}_baseDistribution -i $outdir${filename}.stats -o $outdir${filename}_baseDistribution.png >$outdir${filename}_baseDistribution.png.out 2>$outdir${filename}_baseDistribution.png.err

#echo "done with basedis"

#/opt/fastx/0.0.13.2/bin/fastq_quality_boxplot_graph.sh -t $outdir${filename}_boxWhiskerPlot -i $outdir${filename}.stats -o ${outdir}${filename}_boxWhiskerPlot.png >$outdir${filename}_boxWhiskerPlot.png.out 2>$outdir${filename}_boxWhiskerPlot.png.err

#echo "done with boxplot"

#wc -l $indir${filename} >$indir${filename}.wc
