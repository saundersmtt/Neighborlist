#!/home/m/mwsaunders/Code_Development/NEIGHBOURS/bin/python3 -W ignore::DeprecationWarning

import contacts
import numpy as np
import argparse
import sys
import signal
import logging
import warnings


with warnings.catch_warnings(): 
     warnings.filterwarnings("ignore", category=DeprecationWarning)
     import MDAnalysis
     from MDAnalysis import *

def sigterm_handler(_signo, _stack_frame):
    sys.stderr.write("\nRecieved SIGTERM or SIGINT\n")
    sys.exit(1)

signal.signal(signal.SIGINT, sigterm_handler )
signal.signal(signal.SIGTERM,sigterm_handler)

parser = argparse.ArgumentParser()
parser.add_argument("top",type=str,help="structure file tpr or gro")
parser.add_argument("traj",type=str,help="trajectory file xtc or trr")
parser.add_argument("neighbors",type=argparse.FileType('r'),help="Text file with the list of neighbours")
parser.add_argument("reference",type=str,help="Residue name to look neighbours around it")
parser.add_argument("cutoff", type=float, help="Distance cutoff")
parser.add_argument("name", type=str, help="Name of the data file")
parser.add_argument("-v","--verbose",action="store_true",help="set verbose logging")

args = parser.parse_args()
logger = logging.getLogger(__name__)
if args.verbose:
     logging.basicConfig(level=logging.DEBUG)
else:
     logging.basicConfig(level=logging.CRITICAL)

trajectory = args.traj.split()
topology = args.top

u = Universe(topology,trajectory, continuous = True)
len_traj = len(u.trajectory)
name=args.name

sele1 = u.select_atoms('name {}'.format(args.reference))

neighbours = args.neighbors.read().split()
num_neighbours = len(neighbours)

selection_string=''
for i,neighbour in enumerate(neighbours):
	if i+1 == num_neighbours:
		selection_string += "name {}".format(neighbour)
	else:
		selection_string += "name {} or ".format(neighbour)
sele2 = u.select_atoms('{}'.format(selection_string))

num_atoms_sele1 = len(sele1)
num_atoms_sele2 = len(sele2)

try:
    sele1.write('sele1.gro')
except IndexError:
    print("I found nothing in selection 1! This means there is an error in the neighbors file!")
    exit(100)
try:
    sele2.write('sele2.gro')
except IndexError:
    print("I found nothing in selection 2! This means there is an error in the reference choice!")
    exit(200)

sele1_residues = np.zeros(num_atoms_sele1,dtype=int)
sele1_names = []
for i in range(num_atoms_sele1):
    sele1_residues[i] = sele1.atoms[i].index
    sele1_names.append(sele1.atoms[i].name)

sele2_residues = np.zeros(num_atoms_sele2,dtype=int)
sele2_names = []
for i in range(num_atoms_sele2):
    sele2_residues[i] = sele2.atoms[i].index
    sele2_names.append(sele2.atoms[i].name)

sele1_atoms = list(sele1.atoms.names)
sele2_atoms = list(sele2.atoms.names)

spin="\|/-"

for ts in u.trajectory:
    print(spin[ts.frame%4],end="\r")
    sele1_pos = sele1.positions
    sele2_pos = sele2.positions
    contacts.test(sele1_pos,sele2_pos,sele1_residues,sele2_residues,sele1_names,sele2_names,sele1_atoms,sele2_atoms,args.cutoff,ts.frame,name)
