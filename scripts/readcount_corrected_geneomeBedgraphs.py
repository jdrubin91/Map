from __future__ import division
import os
import glob
import sys
import commands
#python readcount_corrected_geneomeBedgraphs.py directory_of_sortedbams

def origonal(directory_of_sortedbams):
	""" must run genomeCoverageBed.py first"""
	dic_mapped = {}
	list_num = []
	for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):#get number of reads mapped total
		bamfile_root = bamfile.strip(".sorted.bam")
		bamfile_root = bamfile_root.split("/")[-1]
		bowtie_error_file_dir = directory_of_sortedbams.split("/")
		bowtie_error_file_dir = "/".join(bowtie_error_file_dir[0:-2])+"/"
		bowtie_error_file = bowtie_error_file_dir+bamfile_root+".bowtie_v2.stderr"
		f = open(bowtie_error_file)
		f = f.readlines()
		mapped_line = f[4]
		mapped_line = mapped_line.split(" ")
		num =  int(mapped_line[8])
		dic_mapped[bamfile_root] = num
		list_num.append(num)
	max_num = max(list_num)
	for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
		bedgraph1 = bamfile.strip(".sorted.bam")+".pos.BedGraph"
                bedgraph2 = bamfile.strip(".sorted.bam")+".neg.BedGraph"	
		bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
		total_reads = dic_mapped[bamfile_root]
		bedgraphout1 = bedgraph1+".fmpk.BedGraph"
		f = open(bedgraph1)
		wf = open(bedgraphout1, "w")
		for line in f:
			line = line.strip("\n")
			line = line.split("\t")
			chr, start, stop, num_of_reads = line
			size_frag = int(stop)-int(start)
			fpkm_frag = calfpkm(int(num_of_reads), total_reads, size_frag)
			newline = "\t".join([chr, start, stop, str(fpkm_frag)])+"\n"
			wf.write(newline)
		wf.close()
		f.close()
		bedgraphout2 = bedgraph2+".fmpk.BedGraph"
                f = open(bedgraph2)
                wf = open(bedgraphout2, "w")
                for line in f:
                        line = line.strip("\n")
                        line = line.split(" ")
                        chr, start, stop, num_of_reads = line
                        size_frag = int(stop)-int(start)
                        fpkm_frag = calfpkm(int(num_of_reads), total_reads, size_frag)
                        newline = "\t".join([chr, start, stop, str(fpkm_frag)])+"\n"
                        wf.write(newline)
                wf.close()
                f.close()
		

def calfpkm(num_of_reads, total_reads, fragment_size):
        fpkm = int(num_of_reads)/((int(fragment_size)/1000)*(int(total_reads)/1000000))
        return fpkm

def calmp(num_of_reads, total_reads):

        mp = int(num_of_reads)/(int(total_reads)/1000000)
        return mp

def main(directory_of_sortedbams):
	""" must run genomeCoverageBed.py first. fpkm corrects"""
	dic_mapped = {}
	list_num = []
	outdir = os.path.join(directory_of_sortedbams, "genomecoveragebed")
	for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):#find out number of total reads mapped
		bamfile_root = bamfile.strip(".sorted.bam")
		bamfile_root = bamfile_root.split("/")[-1]
		bowtie_error_file_dir = directory_of_sortedbams.split("/")
		bowtie_error_file_dir = "/".join(bowtie_error_file_dir[0:-2])+"/"
		bowtie_error_file = bowtie_error_file_dir+bamfile_root+".bowtie_v2.stderr"
		f = open(bowtie_error_file)
		f = f.readlines()
		mapped_line = f[4]
		mapped_line = mapped_line.split(" ")
		num =  int(mapped_line[8])
		dic_mapped[bamfile_root] = num
		list_num.append(num)
	max_num = max(list_num)
	for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
		bamfileroot = bamfile.split("/")[-1]
		bedgraph1 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".pos.BedGraph"
                bedgraph2 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".neg.BedGraph"	
		bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
		total_reads = dic_mapped[bamfile_root]
		bedgraphout1 = bedgraph1+".fmpk.BedGraph"
		f = open(bedgraph1)
		wf = open(bedgraphout1, "w")
		for line in f:
			line = line.strip("\n")
			line = line.split("\t")
			chr, start, stop, num_of_reads = line
			size_frag = int(stop)-int(start)
			fpkm_frag = calfpkm(int(num_of_reads), total_reads, size_frag)
			newline = "\t".join([chr, start, stop, str(fpkm_frag)])+"\n"
			wf.write(newline)
		wf.close()
		f.close()
		bedgraphout2 = bedgraph2+".fmpk.BedGraph"
                f = open(bedgraph2)
                wf = open(bedgraphout2, "w")
                for line in f:
                        line = line.strip("\n")
                        line = line.split(" ")
                        chr, start, stop, num_of_reads = line
                        size_frag = int(stop)-int(start)
                        fpkm_frag = calfpkm(int(num_of_reads), total_reads, size_frag)
                        newline = "\t".join([chr, start, stop, str(fpkm_frag)])+"\n"
                        wf.write(newline)
                wf.close()
                f.close()

def main2(directory_of_sortedbams):
        """ must run genomeCoverageBed.py first. corrects ignoring lenght of bin"""
        dic_mapped = {}
        list_num = []
        outdir = os.path.join(directory_of_sortedbams, "genomecoveragebed")
	bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):#find out number of total reads mapped
                bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
                bowtie_error_file_dir = directory_of_sortedbams.split("/")
                bowtie_error_file_dir = "/".join(bowtie_error_file_dir[0:-2])+"/"
                bowtie_error_file = bowtie_error_file_dir+bamfile_root+".bowtie_v2.stderr"
                f = open(bowtie_error_file)
                f = f.readlines()
                mapped_line = f[4]
                mapped_line = mapped_line.split(" ")
                num =  int(mapped_line[8])
                dic_mapped[bamfile_root] = num
                list_num.append(num)
        max_num = max(list_num)
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
                bedgraph1 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".pos.BedGraph"
                bedgraph2 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".neg.BedGraph"
		bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.BedGraph'))]
                bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
                total_reads = dic_mapped[bamfile_root]
                bedgraphout1 = bedgraph1+".mp.BedGraph"
		if bedgraph1 in bedgraphs:
	                f = open(bedgraph1)
        	        wf = open(bedgraphout1, "w")
                	for line in f:
                        	line = line.strip("\n")
                        	line = line.split("\t")
                        	chr, start, stop, num_of_reads = line
	                        size_frag = int(stop)-int(start)
        	                fpkm_frag = calmp(int(num_of_reads), total_reads)
                	        newline = "\t".join([chr, start, stop, str(fpkm_frag)])+"\n"
                        	wf.write(newline)
                	wf.close()
                	f.close()
                	bedgraphout2 = bedgraph2+".mp.BedGraph"
                	f = open(bedgraph2)
                	wf = open(bedgraphout2, "w")
                	for line in f:
                        	line = line.strip("\n")
	                        line = line.split(" ")
        	                chr, start, stop, num_of_reads = line
                	        size_frag = int(stop)-int(start)
                        	fpkm_frag = calmp(int(num_of_reads), total_reads)
	                        newline = "\t".join([chr, start, stop, str(fpkm_frag)])+"\n"
        	                wf.write(newline)
                	wf.close()
	                f.close()



def main3(directory_of_sortedbams):
        """ must run genomeCoverageBed.py first. corrects ignoring lenght of bin"""
        dic_mapped = {}
        list_num = []
        outdir = os.path.join(directory_of_sortedbams, "genomecoveragebed")
	bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):#find out number of total reads mapped
                bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
                bowtie_error_file_dir = directory_of_sortedbams.split("/")
                bowtie_error_file_dir = "/".join(bowtie_error_file_dir[0:-2])+"/"
                bowtie_error_file = bowtie_error_file_dir+bamfile_root+".bowtie_v2.stderr"
                f = open(bowtie_error_file)
                f = f.readlines()
                mapped_line = f[4]
                mapped_line = mapped_line.split(" ")
                num =  int(mapped_line[8])
                dic_mapped[bamfile_root] = num
                list_num.append(num)
        max_num = max(list_num)
	bedgraphouts = [filename for filename in glob.glob(os.path.join(outdir, '*.mp.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
                bedgraph1 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".pos.BedGraph"
                bedgraph2 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".neg.BedGraph"
		bedgraph = outdir+"/"+bamfileroot.strip(".sorted.bam")+".BedGraph"
		#print bedgraph1, bedgraph2, "should have been cat together to", bedgraph	# script to do this below..."sh_for_cat_bedgraphs"	
		print bedgraph
		bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
                total_reads = dic_mapped[bamfile_root]
                bedgraphout = bedgraph+".mp.BedGraph"
		if not bedgraphout in bedgraphouts:
	        	f = open(bedgraph)
        		wf = open(bedgraphout, "w")
			line = f.readline()
                	while line:
                        	line = line.strip("\n")
                        	line = line.split("\t")
				if len(line)<3:
					try:
						line = line[0].split(" ")
					except:
						print line
	                        chr, start, stop, num_of_reads = line
        		        frag = calmp(float(num_of_reads), total_reads)
                		newline = "\t".join([chr, start, stop, str(frag)])+"\n"
                        	wf.write(newline)
				line = f.readline()
                	wf.close()
                	f.close()

def main4(directory_of_sortedbams):
        """ must run genomeCoverageBed.py first. corrects ignoring lenght of bin"""
        dic_mapped = {}
        list_num = []
        outdir = os.path.join(directory_of_sortedbams, "genomecoveragebed")
	bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.sort.BedGraph'))]
        for sorted_bam_file_and_path in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = sorted_bam_file_and_path.split("/")[-1]
                bamfileroot = bamfileroot.strip("'*.sorted.bam")
                baminfo = commands.getstatusoutput("samtools flagstat "+sorted_bam_file_and_path)
                baminfo = baminfo[1].split("\n")
                duplicates = baminfo[1]
                mapped_reads =baminfo[2]
                mapped_reads = int(mapped_reads.split(" ")[0])
                print bamfileroot, mapped_reads
                dic_mapped[bamfileroot] = mapped_reads
                list_num.append(mapped_reads)
        max_num = max(list_num)
	bedgraphouts = [filename for filename in glob.glob(os.path.join(outdir, '*.mp.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
                bedgraph1 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".pos.BedGraph"
                bedgraph2 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".neg.BedGraph"
		bedgraph = outdir+"/"+bamfileroot.strip(".sorted.bam")+".bed.sort.BedGraph"
		#print bedgraph1, bedgraph2, "should have been cat together to", bedgraph	# script to do this below..."sh_for_cat_bedgraphs"	
		print bedgraph
		bamfile_root = bamfile.strip(".sorted.bam")
                bamfile_root = bamfile_root.split("/")[-1]
                total_reads = dic_mapped[bamfile_root]
		print total_reads
                bedgraphout = bedgraph+".mp.BedGraph"
		if not bedgraphout in bedgraphouts:
	        	f = open(bedgraph)
        		wf = open(bedgraphout, "w")
			print "createing", bedgraphout
			line = f.readline()
                	while line:
                        	line = line.strip("\n")
                        	line = line.split("\t")
				if len(line)<3:
					try:
						line = line[0].split(" ")
					except:
						print line
	                        chr, start, stop, num_of_reads = line
        		        frag = calmp(float(num_of_reads), total_reads)
                		newline = "\t".join([chr, start, stop, str(frag)])+"\n"
                        	wf.write(newline)
				line = f.readline()
                	wf.close()
                	f.close()


def main5_modifiedforthingsthatendwith15(directory_of_sortedbams):
	#/projects/Down/Downseq/GROseq/gro100814/bowtie2/sortedbam/genomecoveragebed/fortdf
        dic_mapped = {}
        list_num = []
        outdir = os.path.join(directory_of_sortedbams, "/genomecoveragebed/fortdf/")
	outdir = directory_of_sortedbams+"/genomecoveragebed/fortdf/"
	print "outdir is", outdir
	bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.BedGraph'))]
	#GRO177_100814.fastqbowtie2.sorted.bam.flagstat
        for sorted_bam_file_and_path in glob.glob(os.path.join(directory_of_sortedbams, '*sorted.bam.flagstat')):
                bamfileroot = sorted_bam_file_and_path.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
		#GRO177_100814.fastqbowtie2
		f = open(sorted_bam_file_and_path)
		lines = f.readlines()
                mapped_reads =lines[2]
                mapped_reads = int(mapped_reads.split(" ")[0])
		print bamfileroot, mapped_reads
                dic_mapped[bamfileroot] = mapped_reads
                list_num.append(mapped_reads)
		f.close()
        max_num = max(list_num)
	bedgraphouts = [filename for filename in glob.glob(os.path.join(outdir, '*.mp.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*15.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
#		GRO177_100814.fastqbowtie2.BedGraph
		bedgraph = outdir+bamfileroot+".BedGraph"
		print bedgraph
                total_reads = dic_mapped[bamfileroot]
		print total_reads
                bedgraphout = bedgraph+".mp.BedGraph"
		if not bedgraphout in bedgraphouts:
	        	f = open(bedgraph)
        		wf = open(bedgraphout, "w")
			print "createing", bedgraphout
			line = f.readline()
                	while line:
                        	line = line.strip("\n")
                        	line = line.split("\t")
				if len(line)<3:
					try:
						line = line[0].split(" ")
					except:
						print line
	                        chr, start, stop, num_of_reads = line
        		        frag = calmp(float(num_of_reads), total_reads)
                		newline = "\t".join([chr, start, stop, str(frag)])+"\n"
                        	wf.write(newline)
				line = f.readline()
                	wf.close()
                	f.close()





def main5(directory_of_sortedbams):
	#/projects/Down/Downseq/GROseq/gro100814/bowtie2/sortedbam/genomecoveragebed/fortdf
        dic_mapped = {}
        list_num = []
        outdir = os.path.join(directory_of_sortedbams, "/genomecoveragebed/fortdf/")
	outdir = directory_of_sortedbams+"/genomecoveragebed/fortdf/"
	print "outdir is", outdir
	bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.BedGraph'))]
	#GRO177_100814.fastqbowtie2.sorted.bam.flagstat
        for sorted_bam_file_and_path in glob.glob(os.path.join(directory_of_sortedbams, '*sorted.bam.flagstat')):
                bamfileroot = sorted_bam_file_and_path.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
		#GRO177_100814.fastqbowtie2
		f = open(sorted_bam_file_and_path)
		lines = f.readlines()
                mapped_reads =lines[2]
                mapped_reads = int(mapped_reads.split(" ")[0])
                dic_mapped[bamfileroot] = mapped_reads
                list_num.append(mapped_reads)
		f.close()
	print dic_mapped
        max_num = max(list_num)
	bedgraphouts = [filename for filename in glob.glob(os.path.join(outdir, '*.mp.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
#		GRO177_100814.fastqbowtie2.BedGraph
		#bedgraph = outdir+bamfileroot+".sorted.BedGraph"
		bedgraph = outdir+bamfileroot+".BedGraph"
		print bedgraph
		total_reads = dic_mapped[bamfileroot]
		print total_reads
                bedgraphout = bedgraph+".mp.BedGraph"
		if not bedgraphout in bedgraphouts:
	        	f = open(bedgraph)
        		wf = open(bedgraphout, "w")
			print "createing", bedgraphout
			line = f.readline()
                	while line:
                        	line = line.strip("\n")
                        	line = line.split("\t")
				if len(line)<3:
					try:
						line = line[0].split(" ")
					except:
						print line
	                        chr, start, stop, num_of_reads = line
        		        frag = calmp(float(num_of_reads), total_reads)
                		newline = "\t".join([chr, start, stop, str(frag)])+"\n"
                        	wf.write(newline)
				line = f.readline()
                	wf.close()
                	f.close()



def main6(directory_of_sortedbams):
	#/projects/Down/Downseq/GROseq/gro100814/bowtie2/sortedbam/genomecoveragebed/fortdf
        dic_mapped = {}
        list_num = []
        outdir = os.path.join(directory_of_sortedbams, "/genomecoveragebed/fortdf/")
	outdir = directory_of_sortedbams+"/genomecoveragebed/fortdf/"
	print "outdir is", outdir
	bedgraphs = [bedfile for bedfile in glob.glob(os.path.join(outdir, '*.BedGraph'))]
	#GRO177_100814.fastqbowtie2.sorted.bam.flagstat
        for sorted_bam_file_and_path in glob.glob(os.path.join(directory_of_sortedbams, '*sorted.bam.flagstat')):
                bamfileroot = sorted_bam_file_and_path.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
		#GRO177_100814.fastqbowtie2
		f = open(sorted_bam_file_and_path)
		lines = f.readlines()
                mapped_reads =lines[2]
                mapped_reads = int(mapped_reads.split(" ")[0])
                dic_mapped[bamfileroot] = mapped_reads
                list_num.append(mapped_reads)
		f.close()
	print dic_mapped
	for sorted_bam_file_and_path in glob.glob(os.path.join(directory_of_sortedbams, '*.bam.flagstat')):
                bamfileroot = sorted_bam_file_and_path.split("/")[-1]
		bamfileroot = bamfileroot.split(".bam")[0]
		#GRO177_100814.fastqbowtie2
		f = open(sorted_bam_file_and_path)
		lines = f.readlines()
		print sorted_bam_file_and_path
		print lines
                mapped_reads =lines[2]
                mapped_reads = int(mapped_reads.split(" ")[0])
                dic_mapped[bamfileroot] = mapped_reads
                list_num.append(mapped_reads)
		f.close()
	print dic_mapped	
        max_num = max(list_num)
	bedgraphouts = [filename for filename in glob.glob(os.path.join(outdir, '*.mp.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
#		GRO177_100814.fastqbowtie2.BedGraph
		bedgraph = outdir+bamfileroot+".sorted.BedGraph"
		print bedgraph
		total_reads = dic_mapped[bamfileroot]
		print total_reads
                bedgraphout = bedgraph+".mp.BedGraph"
		if not bedgraphout in bedgraphouts:
	        	f = open(bedgraph)
        		wf = open(bedgraphout, "w")
			print "createing", bedgraphout
			line = f.readline()
                	while line:
                        	line = line.strip("\n")
                        	line = line.split("\t")
				if len(line)<3:
					try:
						line = line[0].split(" ")
					except:
						print line
	                        chr, start, stop, num_of_reads = line
        		        frag = calmp(float(num_of_reads), total_reads)
                		newline = "\t".join([chr, start, stop, str(frag)])+"\n"
                        	wf.write(newline)
				line = f.readline()
                	wf.close()
                	f.close()






def sh_for_cat_bedgraphs(directory_of_sortedbams):
	outdir = os.path.join(directory_of_sortedbams, "genomecoveragebed")
	writefile = outdir+"/cat_pos_neg.sh"
	wf = open(writefile, "w")
	for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
                bedgraph1 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".pos.BedGraph"
                bedgraph2 = outdir+"/"+bamfileroot.strip(".sorted.bam")+".neg.BedGraph"
		bedgraph = outdir+"/"+bamfileroot.strip(".sorted.bam")+".bed"
		wline = "cat "+bedgraph1+" "+bedgraph2+" >"+bedgraph+"\n"
		wline2 = "/opt/bedtools/2.16.2/bedtools sort -i "+bedgraph+" > "+bedgraph+".sort.BedGraph\n"
		wf.write(wline)
		wf.write(wline2)
	wf.close()
	print writefile


def sh_for_cat_bedgraphs2(directory_of_sortedbams):
        outdir = os.path.join(directory_of_sortedbams, "genomecoveragebed")
        writefile = outdir+"/cat_pos_neg.sh"
        wf = open(writefile, "w")
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.bam')):
                bamfileroot = bamfile.split("/")[-1]
                bedgraph1 = outdir+"/"+bamfileroot.strip(".bam")+".pos.BedGraph"
                bedgraph2 = outdir+"/"+bamfileroot.strip(".bam")+".neg.BedGraph"
                bedgraph = outdir+"/"+bamfileroot.strip(".sorted.bam")+".bed"
                wline = "cat "+bedgraph1+" "+bedgraph2+" >"+bedgraph+"\n"
                wline2 = "/opt/bedtools/2.16.2/bedtools sort -i "+bedgraph+" > "+bedgraph+".sort.BedGraph\n"
                wf.write(wline)
                wf.write(wline2)
        wf.close()
        print writefile

	

dirs = ["/projects/dowellde/groseq/data/set1/clipped_fastqM10/samfiles/sortedbamfiles/", "/projects/dowellde/groseq/data/set2/samfiles/sortedbamfiles/","/projects/dowellde/groseq/data/set3/samfiles/sortedbamfiles/", "/projects/dowellde/groseq/data/set4/samfiles/sortedbamfiles/", "/projects/dowellde/groseq/data/set5/samfiles/sortedbamfiles/"]


def run_bunch():
	for dir in dirs[3:]:
		main2(dir)
#	main(dirs[0])

if __name__=="__main__":
#	try:
#	sh_for_cat_bedgraphs2(sys.argv[1])
#	main4(sys.argv[1])
	main5(sys.argv[1])
#	main6(sys.argv[1])
#	main5_modifiedforthingsthatendwith15(sys.argv[1])
#	except:
#		print "python readcount_corrected_geneomeBedgraphs.py <directory_of_sortedbams>"

