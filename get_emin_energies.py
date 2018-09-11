'''
Elliot Williams
4th September 2018
get_emin_energies.py

This script uses a regular expression to extract the energies associated with
energy minimization as run in AMBER from the output files, and then graphs them
and outputs the associated plot into a subdirectory within the `EMIN` dir.

For each step in the energy minimization, the color alternates, starting with
red and then going to blue and back to red, etc.
'''

import glob
import re
import os
import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt

def grab_energies(filename):
    f = open(filename, 'r')
    energies = []

    for line in f:
        if "EAMBER" in line:
            try:
                energy = float(line.split("=")[1].strip())
            except ValueError:
                energy = 0
            energies.append(energy)

    return energies

def plot_energies(title, subtitle, energies, outfile):
    iterations = [x for x in range(len(energies))]
    plt.plot(iterations, energies, 'ro')

if __name__ == "__main__":
    energy_files = glob.glob("EMIN/*_emin*.out")
    energy_nums = [int(re.sub("[^0-9]", "", x)) for x in energy_files]
    energy_files = [x for _,x in sorted(zip(energy_nums,energy_files))]

    curr_cycle = 0

    is_red = False

    for file in energy_files:
        cycle = re.findall("(?<=emin)[0-9]{1,2}", file)[0]
        curr_energies = grab_energies(file)
        curr_iterations = [x + curr_cycle for x in range(len(curr_energies))]
        curr_cycle += len(curr_energies)

        if not is_red:
            plt.plot(curr_iterations, curr_energies, 'ro')
            is_red = True
        else:
            plt.plot(curr_iterations, curr_energies, 'bo')
            is_red = False

    outfile = "EMIN/energy_plots/emin.png"

    plt.xlabel('Cycle')
    plt.ylabel('Energy (kcal)')
    path = os.getcwd().split('/')
    plt.title("{} for {}".format("Energy Minimization", path[len(path)-1]))
    plt.savefig(outfile)
    plt.close()
