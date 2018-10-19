from __future__ import division
import os
import glob
import sys

#Calculates millions mapped reads
def calmp(num_of_reads, total_reads):
        mp = int(num_of_reads)/(int(total_reads)/1000000)
        return mp

#Normalize bedgraphs to millions mapped reads
def main(directory_of_sortedbams):
        dic_mapped = {}
        list_num = []
	outdir = directory_of_sortedbams + "/genomecoveragebed/TDF/"
	print "outdir is", outdir
        for sorted_bam_file_and_path in glob.glob(os.path.join(directory_of_sortedbams, '*sorted.bam.flagstat')):
                bamfileroot = sorted_bam_file_and_path.split("/")[-1].split(".sorted")[0]
		f = open(sorted_bam_file_and_path)
		lines = f.readlines()
                mapped_reads = int(lines[2].split(" ")[0])
                dic_mapped[bamfileroot] = mapped_reads
                list_num.append(mapped_reads)
		f.close()
	bedgraphouts = [filename for filename in glob.glob(os.path.join(outdir, '*.mp.BedGraph'))]
        for bamfile in glob.glob(os.path.join(directory_of_sortedbams, '*.sorted.bam')):
                bamfileroot = bamfile.split("/")[-1]
		bamfileroot = bamfileroot.split(".sorted")[0]
		bedgraph = outdir+bamfileroot+".sorted.BedGraph"
		print bedgraph
                total_reads = dic_mapped[bamfileroot]
		print total_reads
                bedgraphout = bedgraph+".mp.BedGraph"
		if not bedgraphout in bedgraphouts:
	        	f = open(bedgraph)
        		wf = open(bedgraphout, "w")
			print "creating", bedgraphout
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



if __name__=="__main__":
	main(sys.argv[1])

