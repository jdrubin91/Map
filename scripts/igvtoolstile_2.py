import sys
import os
import glob


def tiledir2(genome, directory_of_BedGraphs):
	wf = open(directory_of_BedGraphs+"igvtoolstile.sh", "w")
        for bedGraphfile in glob.glob(os.path.join(directory_of_BedGraphs, '*mp.BedGraph')):
                wf.write("/opt/igvtools/2.1.24/igvtools toTDF "+bedGraphfile+" "+bedGraphfile+".tdf /opt/igvtools/2.1.24/genomes/"+genome+".genome &\n\n")
	wf.close()


if __name__=="__main__":
	tiledir2(sys.argv[1],sys.argv[2])


