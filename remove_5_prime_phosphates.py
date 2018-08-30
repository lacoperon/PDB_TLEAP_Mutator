'''
Elliot Williams
August 29th, 2018
5' PO4 3- Removal Script

This Python file exists to allow us to remove the 5' phosphate groups from
nucleotide chains within PDB files we are attempting to import into TLEAP .

We do this because tleap won't accept any input nucleotide chain in which there
is a 5' phosphate group.

This script was originally intended to work 'in place', but I realize that
doing so prevents assurances that it was run in the first place. So, new files
will be created.
'''

import sys

def remove_phosphates(input_file, output_file):

    lines = open(input_file).readlines()
    output_lines = []

    after_ter = True
    after_resid = None
    i = 0
    while i < len(lines):
        line = lines[i]
        resid = line[21:26]
        atom_name = line[13:16]
        # print(atom_name)

        if after_ter:
            after_resid = resid
            after_ter = False

        if "TER" in line:
            after_ter = True
            print("TER HIT")

        if after_resid == resid and atom_name in ["P","OP1","OP2","OP3"]:
            print("Deleting {} at {}".format(atom_name, resid))
            
        else:
            output_lines.append(line)

        i += 1

    out_content = "".join(output_lines)
    out_writer = open(output_file, "w")
    out_writer.write(out_content)
    out_writer.close()



if __name__ == "__main__":
    assert len(sys.argv) >= 2

    input_files  = sys.argv[1:]
    output_files = [x.split(".")[0] + "_pfilt.pdb" for x in input_files]

    for i in range(len(input_files)):
        remove_phosphates(input_files[i], output_files[i])
