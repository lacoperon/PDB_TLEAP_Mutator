'''
Elliot Williams
August 29th, 2018
5' PO4 3- Removal Script

This Python file exists to allow us to remove the 5' phosphate groups from
nucleotide chains within PDB files we are attempting to import into TLEAP .

We do this because tleap won't accept any input nucleotide chain in which there
is a 5' phosphate group.

This script works 'in place', so you only need to specify the name of the file
you're attempting to alter.
'''

def remove_phosphates(pdb_file):
    f = open(pdb_file, "r")

    for line in f:
        print(line)

remove_phosphates()
