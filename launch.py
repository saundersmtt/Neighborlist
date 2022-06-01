#!/home/m/mwsaunders/Code_Development/NEIGHBOURS/bin/python

import os
from MDAnalysis import *
import MDAnalysis
import argparse
import subprocess
import sys
import progressbar
import time
 

def check_process(name):
    output = []
    cmd = "ps -aef | grep -i '%s' | grep -v 'grep' | awk '{ print $2 }' > /tmp/out"
    os.system(cmd % name)
    with open('/tmp/out', 'r') as f:
        line = f.readline()
        while line:
            output.append(line.strip())
            line = f.readline()
            if line.strip():
                output.append(line.strip())

    return output

parser = argparse.ArgumentParser()
parser.add_argument("--top",type=str,help="structure file tpr or gro")
parser.add_argument("--traj",type=str,help="trajectory file xtc or trr")
parser.add_argument("--neighbour_file",type=str,help="Text file with the list of neighbours")
parser.add_argument("--reference_residue",type=str,help="Residue name to look neighbours around it")
parser.add_argument("--cutoff", type=float, help="Distance cutoff")
parser.add_argument("--cores", type=int, help="Number of cores to split trajectory analysis to")   
args = parser.parse_args()

trajectories=args.traj
topology=args.top

u = Universe(topology, trajectories.split(), convert_units = False, continuous=True)
len_traj = len(u.trajectory)
#len_traj= args.length
step = len_traj//args.cores
print(len_traj, args.cores, step)

for i in range(args.cores):
    initial = i*step
    name = str(i)+'_tmp'
    if i == args.cores-1:
        final = len_traj
    else:
        final = i*step+step
    os.system('echo /home/m/mwsaunders/Code_Development/NEIGHBOURS/template.py {} "{}" {} {} {} {} {} {} &'\
            .format(topology,trajectories,args.neighbour_file,args.reference_residue,initial,final,args.cutoff,name))



exit(0)
