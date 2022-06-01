#!/home/m/mwsaunders/Code_Development/NEIGHBOURS/bin/python

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("cores", type=int, help="Number of cores to use")
args = parser.parse_args()

for i in range(args.cores):
    os.system("cat {}_tmp.txt >> datam.txt".format(i))
    os.system("rm {}_tmp.txt".format(i))
os.system("echo END >> datam.txt")
