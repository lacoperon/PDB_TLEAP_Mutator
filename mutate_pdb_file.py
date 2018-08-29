'''
Elliot Williams
August 29th, 2018
PDB Nucleotide Mutator

This Python file exists to allow us to `make` tleap interpret nucleotides
of one type as another type, via changing some atom and residue names,
as well as deleting some lines, within the source PDB files.

This script is intentionally not generalizable, because different nucleotide
modifications require different line replacements, and PDB files themselves are
not always formatted the same way.
'''

import re
import sys
from functools import partial

'''
This function alters a PDB file to make one type of residue be interpreted
as another type when passed into TLEAP.

Input:
    resid        : chain name and residue number unique ID (IE 'D 711')
    delete_atms  : list of atoms that should be deleted (ie ["N6"])
    rename_atms  : list of atoms that should be renamed (ie ["C4"])
    renamed_atms : list of renamed atoms relative to rename_atms (ie ["C6"])
    line         : input line from PDB file
'''

def mutate_residue(resid, delete_atms, rename_atms, renamed_atms, line):
    if "A E6956" in line:
        atom_type = line.split()[2]

        delete_atms = ["N6"]
        rename_atms = []


        if atom_type in []

if __name__ == "__main__":
    assert len(sys.argv) == 3
    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    content = open(input_file).readlines()
    content = [mutate_residue(line) for line in content]
    # content = mutate_residues_
