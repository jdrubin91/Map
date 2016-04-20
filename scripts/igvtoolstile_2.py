import sys
import os
import glob

#python igvtoolstile.py <directory_of_BedGraphs>


def tiledir2(directory_of_BedGraphs):
	wf = open(directory_of_BedGraphs+"igvtoolstile.sh", "w")
        for bedGraphfile in glob.glob(os.path.join(directory_of_BedGraphs, '*mp.BedGraph')):
                wf.write("/opt/igvtools/2.1.24/igvtools toTDF "+bedGraphfile+" "+bedGraphfile+".tdf /opt/igvtools/2.1.24/genomes/hg19.genome &\n\n")
		#wf.write("/opt/igvtools/2.1.24/igvtools toTDF "+bedGraphfile+" "+bedGraphfile+".tdf /opt/igvtools/2.1.24/genomes/mm10.genome &\n\n")
		#wf.write("/opt/igvtools/2.1.24/igvtools toTDF "+bedGraphfile+" "+bedGraphfile+".tdf /opt/igvtools/2.1.24/genomes/dm3.genome &\n\n")
	wf.close()


if __name__=="__main__":
	tiledir2(sys.argv[1])


