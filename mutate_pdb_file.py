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

So, if you're using this, make sure you understand how it works first and
generate the appropriate parameters for `mutate_residue` by hand.
Then you should be golden.
'''

import re
import sys
from functools import partial
'''
This function alters a PDB file to make one type of residue be interpreted
as another type when passed into TLEAP.

Input:
    resid        : chain name and residue number unique ID   (IE 'A 711')
    newid        : desired chain name and residue number ID  (IE 'G 711')
    delete_atms  : list of atoms that should be deleted (ie ["N6"])
    rename_atms  : list of atoms that should be renamed (ie ["C4"])
    renamed_atms : list of renamed atoms relative to rename_atms (ie ["C6"])
    line         : input line from PDB file
'''

def mutate_residue(resid, newid,  delete_atms, rename_atms, renamed_atms, line):
    assert len(rename_atms) == len(renamed_atms)
    if resid in line:
        atom_type = line.split()[2]

        if atom_type in delete_atms:
            return ''
        elif atom_type in rename_atms:
            # Gets the index of atom_type in rename_atms, and gets appropriate
            # corresponding item in renamed_atms
            replace_type = renamed_atms[rename_atms.index(atom_type)]
            line = line.replace(atom_type, replace_type, 1)

        return line.replace(resid, newid, 1)
    else:
        return line


if __name__ == "__main__":

    assert len(sys.argv) == 3
    input_file  = sys.argv[1]
    output_file = sys.argv[2]
    print("Input: {}\nOutput: {}".format(input_file, output_file))

    # Defines partial functions in terms of the mutations we want to make
    # within the PDB files (ie each one of these parameters is hand verified)
    mut_A_to_G = partial(mutate_residue, "A E6956", "G E6956", ["N6"],[],[])
    mut_A_to_C = partial(mutate_residue, "A E6957", "C E6957",
                         ["N1","C2","N3","C5","C6","N6"],
                         ["C4","N7","C8","N9"],
                         ["C6","N3","C2","N1"])

    content = open(input_file,"r").readlines()

    print(len(content))

    print("Mutation: A E6956 --> G E6956")
    content = [mut_A_to_G(line) for line in content]
    content = list(filter(lambda x : x != None, content))
    print(len(content))
    print("Mutation: A E6957 --> C E6957")
    content = [mut_A_to_C(line) for line in content]
    content = list(filter(lambda x : x != None, content))

    print(len(content))

    out_content = "".join(content)
    out_writer = open(output_file, "w")
    out_writer.write(out_content)
    out_writer.close()
