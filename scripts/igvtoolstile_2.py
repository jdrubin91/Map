import sys
import os
import glob


def tiledir2(genome, directory_of_BedGraphs,e_and_o,email):
    outfile = open(directory_of_BedGraphs+"igvtoolstile.sh", "w")
    # outfile.write("#!/bin/bash\n")
    # outfile.write("#SBATCH -p long\n")
    # outfile.write("#SBATCH --nodes=1\n")
    # outfile.write("#SBATCH --ntasks=1\n")
    # outfile.write("#SBATCH --output " + e_and_o + "%x.out\n")
    # outfile.write("#SBATCH --error " + e_and_o + "%x.err\n")
    # outfile.write("#SBATCH --mail-type=ALL\n")
    # outfile.write("#SBATCH --mail-user=" + email + "\n")
    outfile.write("module load igvtools/2.3.75\n")
    for bedGraphfile in glob.glob(os.path.join(directory_of_BedGraphs, '*mp.BedGraph')):
        outfile.write("/opt/igvtools/2.3.75/igvtools toTDF " + bedGraphfile + " " + bedGraphfile + ".tdf /opt/igvtools/2.3.75/genomes/" + genome + ".chrom.sizes &\n\n")
    outfile.close()


if __name__=="__main__":
	tiledir2(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
