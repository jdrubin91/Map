__author__ = 'Jonathan Rubin'

import os

def run(scriptdir, genomedir, bowtieindex, bowtieoptions, email, e_and_o, fullpath):
    outfile = open(scriptdir + 'bam_to_5primebed.sbatch', 'w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load bedtools/2.25.0\n")
    outfile.write("module load gcc/7.2.0\n")
    outfile.write("genome=" + genomedir + "\n")
    outfile.write("echo $infile\n")
    outfile.write("echo $genome\n")
    outfile.write("echo $outfile1\n")
    outfile.write("mkdir -p  $outdir/genomecoveragebed\n")
    outfile.write("mkdir -p $outdir/forFstitch\n")
    outfile.write("mkdir -p $outdir/fortdf\n")
    outfile.write("genomeCoverageBed -5 -bg -strand + -ibam $infile -g $genome > $outdir/forFstitch/$outfile1\n")
    outfile.write("genomeCoverageBed -5 -bg -strand - -ibam $infile -g $genome > $outdir/forFstitch/$outfile2\n")
    outfile.write("genomeCoverageBed -bg -strand + -ibam $infile -g $genome > $outdir/genomecoveragebed/$outfile3\n")
    outfile.write("genomeCoverageBed -bg -strand - -ibam $infile -g $genome | awk -F '\t' -v OFS='\t' '{ $4 = - $4 ; print $0 }'> $outdir/genomecoveragebed/$outfile4\n")
    outfile.write("cat $outdir/genomecoveragebed/$outfile4 $outdir/genomecoveragebed/$outfile3 > $outdir/fortdf/$outfile5.bed\n")
    outfile.write("sortBed -i $outdir/fortdf/$outfile5.bed >$outdir/fortdf/$outfile5\n")
    outfile.close()

    outfile = open(scriptdir + 'rseqc.sbatch', 'w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=64\n")
    outfile.write("#SBATCH --mem=500gb\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load python/2.7.14\n")
    outfile.write("module load python/2.7.14/rseqc/2.6.4\n")
    outfile.write("module load python/2.7.14/bx-python/0.7.3\n")
    outfile.write("module load samtools/1.3.1\n")
    outfile.write("echo $infile\n")
    outfile.write("echo $genefile\n")
    outfile.write("echo $rRNAfile\n")
    outfile.write("echo $ofile\n")
    outfile.write("/opt/rseqc/python-2.7.14/2.6.4/bin/bam_stat.py -i ${infile} > ${ofile}.bam_stat.txt\n")
    outfile.write("/opt/rseqc/python-2.7.14/2.6.4/bin/read_distribution.py -i ${infile} -r ${genefile} > ${ofile}.read_distribution.txt\n")
    outfile.write("/opt/rseqc/python-2.7.14/2.6.4/bin/read_duplication.py -i ${infile} -o ${ofile}\n")
    outfile.write("/opt/rseqc/python-2.7.14/2.6.4/bin/split_bam.py -i ${infile} -r ${rRNAfile} -o ${ofile}\n")
    outfile.write("samtools flagstat ${ofile}.ex.bam > ${ofile}.ex.bam.flagstat\n")
    outfile.write("samtools flagstat ${ofile}.in.bam > ${ofile}.in.bam.flagstat\n")
    outfile.write("samtools flagstat ${ofile}.junk.bam > ${ofile}.junk.bam.flagstat\n")
    outfile.close()
    
    outfile = open(scriptdir + 'bowtieafastq.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=32\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load bowtie/2.2.9\n")
    outfile.write("echo $fastq1pathandfile\n")
    outfile.write("echo ${outdir}${outfile}.sam\n")
    # outfile.write("/opt/bowtie/bowtie2-2.0.2/bowtie2 -p32 " + bowtieoptions + " -un ${outdir}${outfile}.unmapped.fastq \\\n")
    outfile.write("/opt/bowtie/2.2.9/bowtie2 -p32 " + bowtieoptions + " \\\n")
    outfile.write("-x " + bowtieindex + " \\\n")
    outfile.write("-U $fastq1pathandfile \\\n")
    outfile.write("-S ${outdir}${outfile}.sam \\\n")
    outfile.write("2> ${outdir}${outfile}.stderr\n")
    outfile.close()

    outfile = open(scriptdir + 'trim_galore.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load python/2.7.14/cutadapt\n")
    outfile.write("module load python/2.7.14/xopen/0.1.0\n")
    outfile.write("module load trim_galore/0.4.3\n")
    outfile.write("module load python/2.7.14\n")
    outfile.write("trim_galore --path_to_cutadapt /opt/cutadapt/python-2.7.14/1.12/bin/cutadapt -o $outdir $infile\n")
    outfile.close()

    outfile = open(scriptdir + 'trimmomatic.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load trim_galore/0.4.3\n")
    outfile.write("java -XX:ParallelGCThreads=1 -jar /opt/trimmomatic/0.32/trimmomatic-0.32.jar SE $infile $outdir ILLUMINACLIP:Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10\n")
    outfile.close()

    outfile = open(scriptdir + 'samtobai.sbatch', 'w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=64\n")
    outfile.write("#SBATCH --mem=500gb\n")
    outfile.write("#SBATCH --time=96:00:00\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load samtools/1.3.1\n")
    outfile.write("mkdir -p $outdir\n")
    outfile.write("samtools view -S -b -o ${outdir}${basename}.bam ${indir}${basename}.sam 2>${outdir}${basename}.bam.err\n")
    outfile.write("samtools sort -m500G -o ${outdir}${basename}.sorted.bam ${outdir}${basename}.bam\n")
    outfile.write("samtools flagstat ${outdir}${basename}.bam > ${outdir}${basename}.bam.flagstat 2>${outdir}${basename}.bam.flagstat.err\n")
    outfile.write("samtools index ${outdir}${basename}.sorted.bam\n")
    outfile.write("samtools flagstat ${outdir}${basename}.sorted.bam > ${outdir}${basename}.sorted.bam.flagstat 2>${outdir}${basename}.sorted.bam.flagstat.err\n")
    outfile.close()

    outfile = open(scriptdir + 'flipfastq.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load fastx-toolkit/0.0.13\n")
    outfile.write("/opt/fastx-toolkit/0.0.13/bin/fastx_reverse_complement -Q33 -i $infile -o ${outdir}${outfile}\n")
    outfile.write("wc1=`wc -l $infile | awk '{print $1}'`\n")
    outfile.write("wc2=`wc -l ${outdir}${outfile} | awk '{print $1}'`\n")
    outfile.write("if [ $wc1 -ne $wc2 ]\n")
    outfile.write("then\n")
    outfile.write('echo "error lines dont match"\n')
    outfile.write("echo $infile\n")
    outfile.write("echo $wc1\n")
    outfile.write("echo ${outdir}${outfile}\n")
    outfile.write("echo $wc2\n")
    outfile.write("fi\n")
    outfile.close()

    outfile = open(scriptdir + 'qual.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load fastqc/0.11.5\n")
    outfile.write("echo $indir${filename}\n")
    outfile.write("echo $outdir${filename}.stats\n")
    outfile.write("/opt/fastqc/0.11.5/fastqc $indir${filename} -o $outdir\n")
    outfile.close()

    outfile = open(scriptdir + 'preseq.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load preseq/2.0.3\n")
    outfile.write("/opt/preseq/2.0.3/preseq c_curve -B -o ${ofile}.c_curve.txt ${infile}${filename}\n")
    outfile.write("/opt/preseq/2.0.3/preseq lc_extrap -B -o ${ofile}.lc_extrap.txt ${infile}${filename}\n")
    outfile.write("/opt/preseq/2.0.3/preseq gc_extrap -B -o ${ofile}.gc_extrap.txt ${infile}${filename}\n")
    outfile.close()

    outfile = open(scriptdir + 'sradump.sbatch','w')
    outfile.write("#!/bin/bash\n")
    outfile.write("#SBATCH -p long\n")
    outfile.write("#SBATCH --nodes=1\n")
    outfile.write("#SBATCH --ntasks=1\n")
    outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    outfile.write("#SBATCH --mail-type=ALL\n")
    outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load sra/2.8.0\n")
    outfile.write("/opt/sra/2.8.0/bin/fastq-dump -O $outdir $infile\n")
    outfile.close()

