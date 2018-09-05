'''
Elliot Williams
4th September 2018
get_emin_energies.py

This script uses a regular expression to extract the energies associated with
energy minimization as run in AMBER from the output files, and then graphs them
and outputs the associated plots into a subdirectory within the `EMIN` dir.
'''

import glob
import re
import os
import matplotlib.pyplot as plt

def grab_energies(filename):
    f = open(filename, 'r')
    energies = []

    for line in f:
        if "EAMBER" in line:
            energy = float(line.split("=")[1].strip())
            energies.append(energy)

    return energies

def plot_energies(title, subtitle, energies, outfile):
    iterations = [x for x in range(len(energies))]
    plt.plot(iterations, energies, 'ro')
    plt.xlabel('Cycle')
    plt.ylabel('Energy (kcal)')
    plt.title("{}\n{}".format(title, subtitle))
    plt.savefig(outfile)


if __name__ == "__main__":
    energy_files = glob.glob("EMIN/*_emin*.out")

    for file in energy_files:
        cycle = re.findall("(?<=emin)[0-9]{1,2}", file)[0]
        energies = grab_energies(file)
        title = "EMIN Cycle {}".format(cycle)
        path = os.getcwd().split('/')
        subtitle = "Within {}".format(path[len(path)-1])

        plot_energies(title, subtitle, energies,
                      "EMIN/energy_plots/emin{}.jpg".format(cycle))
