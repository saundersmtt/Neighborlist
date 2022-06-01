#!/home/m/mwsaunders/Code_Development/NEIGHBOURS/bin/python
import numpy as np
from collections import defaultdict
import argparse
import os
import subprocess as sp
import progressbar as pb

parser = argparse.ArgumentParser()
parser.add_argument("infile",type=str,help="Input file")
parser.add_argument("neighbour_file",type=argparse.FileType('r'),help="Text file with the list of neighbours")
parser.add_argument("outfile",type=str,help="Output file")
args = parser.parse_args()

count_dict = defaultdict(list)
neighbours = args.neighbour_file.read().split()
num_neighbours = len(neighbours)
outfile=args.outfile

fout = open(outfile,'w')
#count = sp.run('/usr/bin/wc -l {}'.format(args.infile),stdout=sp.PIPE)
#count = os.popen("wc -l {}".format(args.infile)).read().split()[0]
#print(count)
#pbar = pb.ProgressBar(maxval=int(count)).start()
i=0
with open(args.infile,'r') as f:
    for num_line,line in enumerate(f):
#        i=i+1
#        pbar.update(i)
        if num_line == 0:
            pass
        elif num_line == 1:
            reference_atom = line.split()[0]
        else:
            break

fout.write("#{:<5s}".format(reference_atom))
for neighbour in neighbours:
    fout.write("{:>5s}".format(neighbour))
fout.write("{:^16s}\n".format("Z-pos"))

def print_to_file(ugly_struct):
    for reference in ugly_struct:
        fout.write("{:5s}".format(reference))
        for neighbour in ugly_struct[reference][0][0]:
            fout.write("{:5d}".format(neighbour))
        fout.write("{:16.8f}\n".format(ugly_struct[reference][0][1]))

count_dict = defaultdict(list)
i=0
frameindex=0
with open(args.infile,'r') as f:
    for line in f:
        data = line.split()
        if len(data) == 1:
            if frameindex > 1: 
                 fout.write("{};;\n".format(frameindex))
            frameindex += 1
            print_to_file(count_dict)
            count_dict = defaultdict(list)
        else:
            for i,neighbour in enumerate(neighbours):
                if data[6] == neighbour:
                    if len(count_dict[data[1]])==0:
                        count_dict[data[1]].append([np.zeros(num_neighbours,dtype=int),float(data[11])])
                        count_dict[data[1]][0][0][i]+=1
                    else:
                        count_dict[data[1]][0][0][i]+=1

fout.close()
