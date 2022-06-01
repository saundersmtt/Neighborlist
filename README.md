1) Modify neighbours_list.txt to get the neighbours you want around a reference residue name
2) python setup.py build_ext --inplace # This builds the contacts cython code
3) python launch.py start.tpr start.xtc neighbours_list.txt LI 3.3 16 # Arguments are as follows {.tpr} {.xtc} {neighbours_list.txt} {resname of reference residue} {distance cutoff} {number of cores}
4) Visually inspect sele1.gro and sele2.gro to verify your selection
5) python join.py 16 # Arguments are as follows {number of files to join usually should be the same as number of cores used in 2)}
6) python count.py neighbours_list.txt # Arguments are as follows {neighbours_list.txt should be the same file as the one in 2)}

python executable should have a mdanalysis 2.0


