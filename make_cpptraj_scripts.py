"""
Elliot Williams
20th September 2018
make_cpptraj_scripts.py

This script creates the correct cpptraj input (.in) files for AMBER 16, in
our 5JU*_GC Korostelev N1 subsystem.
It also generates the correct BASH (.sh) file to submit the job to the cluster.

It generates the `cpptraj` analysis files in all subdirectories of `NEUTRAL`.
"""

import glob
import os

def make_cpptraj_in(struct_name, directory):
    script_text = """
parm ../../TLEAP/{0}_gc_wat.prmtop [modi3]
trajin mdcrd parm [modi3] [modi33]
autoimage


rms all_resid :1-495@N,CA,C,P,O5,O3 out data/rmsd_all.dat
rms restr_resid :1-5,11-17,22-33,35,39-41,73-95,98-101,108-126,130-132,139-146,153-162,165-166,170-171,184-187,204-215,227-242,252-265,269-312,330-343,350-360,372-377,379-444,451-479,494-495@N,CA,C,O,P,O5,O3,C5 out data/rmsd_restr.dat
rms unrestr_resid :6-10,18-21,34,36-38,42-72,96-97,102-107,127-129,133-138,147-152,167-169,172-183,188-203,216-226,243-251,266-268,313-329,344-349,361-371,378,445-450,480-493@N,CA,C,O,P,O5,O3,C5 out data/rmsd_NOTrestr.dat

rms unrestr_nt :6-10,18-21,34,36-38,42-72,96-97,102-107,127-129,133-138,147-152,167-169,172-183@P,O5,O3,C5 out data/rmsd_NOTrestr_nucleotides.dat
rms unrestr_aminoacids :188-203,216-226,243-251,266-268,313-329,344-349,361-371,378,445-450,480-493@N,CA,C,O out data/rmsd_NOTrestr_aminoacids.dat



#hbond nhb_528_527 :59,60,54,53 out data/nhb_528_527.dat
hbond nhb_528 :60@O2,N3,N4|:53@N2,N1,O6 out data/nhb_528.dat #angle 20
hbond nhb_527 :59@N2,N1,O6|:54@O2,N3,N4 out data/nhb_527.dat #angle 20
#hbond nhb_529 :61,52 out data/nhb_529.dat

#hbond nhb_ss522 :54@O4'|:53@O2' out data/nhb_ss522_1.dat
#hbond nhb_ss523 :55@O4'|:54@O2' out data/nhb_ss523_2.dat

hbond nhb_1054 :178@N2,N1,O6|:105@O2,N3,N4 out data/nhb_1054.dat #angle 20


atomicfluct out data/B_fac.apf @C,N,P byres bfactor

#mid-basepair distance
distance d527_522 :59@N1 :54@N3 out data/dist_527_N1_522_N3.dat

#distance d527_Asp247 :59@O6 :247@CB out data/dist_527_Asp247.dat
#INCORRECTaadistance d529_Asp196 :59@O6 :196@ND2 out data/dist_527_Asp196.dat


#Asp116(247of495) to 527
distance d527_O6_Asp116_CA :59@O6 :247@CA out data/dist_527_O6_Asp116_CA.dat
distance d527_N2_Asp116_CA :59@N2 :247@CA out data/dist_527_N2_Asp116_CA.dat  #swiveled 527 interacts with AspCA**

#Asp116(247of495) to 522
distance d522_N4_Asp116_CA :54@N4 :247@CA out data/dist_522_N4_Asp116_CA.dat  #general Asp
distance d522_N4_Asp116_CG :54@N4 :247@CG out data/dist_522_N4_Asp116_CG.dat  #swiveled Asp
distance d522_N4_Asp116_OD1 :54@N4 :247@OD1 out data/dist_522_N4_Asp116_OD1.dat  #swiveled Asp


#Asp116(247of495) to 523 neighbor
distance d523_N6_Asp116_CA :55@N6 :247@CA out data/dist_523_N6_Asp116_CA.dat  #general Asp
distance d523_N6_Asp116_CG :55@N6 :247@CG out data/dist_523_N6_Asp116_CG.dat  #swiveled Asp
distance d523_N6_Asp116_OD1 :55@N6 :247@OD1 out data/dist_523_N6_Asp116_OD1.dat  #swiveled Asp



#Asn65(196of495)
distance d527_O6_Asn65_CA :59@O6 :196@CA out data/dist_527_O6_Asn65_CA.dat #backbone Asn

#distance d527_N7_Asn65_HD21 :59@N7 :196@HD21 out data/dist_527_N7_Asn65_HD21.dat
#distance d527_O6_Asn65_HD21 :59@O6 :196@HD21 out data/dist_527_O6_Asn65_HD21.dat
distance d527_O6_Asn65_ND2 :59@O6 :196@ND2 out data/dist_527_O6_Asn65_ND2.dat


distance d528_N4_Asn65_CA :60@N4 :196@CA out data/dist_528_N4_Asn65_CA.dat  #backbone Asn

#distance d528_H42_Asn65_OD1 :60@H42 :196@OD1 out data/dist_528_H42_Asn65_OD1.dat
distance d528_N4_Asn65_OD1 :60@N4 :196@OD1 out data/dist_528_N4_Asn65_OD1.dat


#bottom of base pair related to propeller and stagger
#distance d527_O6_523 :59@O6 :55@H61 out data/dist_527_O6_523_H61.dat
#distance d527_O6_522_H41 :59@O6 :54@H41 out data/dist_527_O6_522_H41.dat
#heavy atom vs
distance d527_O6_523_N6 :59@O6 :55@N6 out data/dist_527_O6_523_N6.dat
distance d527_O6_522_N4 :59@O6 :54@N4 out data/dist_527_O6_522_N4.dat


#other 527:522 H-bonds
#distance d527_H21_522_O2 :59@H21 :54@O2 out data/dist_527_H21_522_O2.dat
#distance d527_H1_522_N3 :59@H1 :54@N3 out data/dist_527_H1_522_N3.dat
#heavy atom vs
distance d527_N2_522_O2 :59@N2 :54@O2 out data/dist_527_N2_522_O2.dat
distance d527_N1_522_N3 :59@N1 :54@N3 out data/dist_527_N1_522_N3.dat


#H-bonds between adjacent bases
#distance d527_O6_528_H42 :59@O6 :60@H42 out data/dist_527_O6_528_H42.dat
#distance d522_O6_523_H42 :53@O6 :54@H42 out data/dist_522_O6_523_H42.dat
#heavy atom vs
distance d527_O6_528_N4 :59@O6 :60@N4 out data/dist_527_O6_528_N4.dat
distance d522_O6_523_N4 :53@O6 :54@N4 out data/dist_522_O6_523_N4.dat

#sugar to sugar
distance d522_O2'_523_O4' :53@O2' :54@O4' out data/dist_522_O2'_523_O4'.dat
distance d521_O2'_522_O4' :52@O2' :53@O4' out data/dist_521_O2'_522_O4'.dat


#RNA geometry
nastruct resrange 59,60,54,53 naout data/nastruct_59_60_54_53.dat #noheader
nastruct resrange 59,54 naout data/nastruct_59_54.dat #noheader
nastruct resrange 60,53 naout data/nastruct_60_53.dat #noheader

#dihedrals
dihedral dh529_axis1 :112@P :415@CA :302@CA :61@N1 out data/dihedral_529_axis1.dat
dihedral dh528_axis1 :112@P :415@CA :302@CA :60@N3 out data/dihedral_528_axis1.dat
dihedral dh527_axis1 :112@P :415@CA :302@CA :59@N1 out data/dihedral_527_axis1.dat

dihedral dh530_529 :62@N1 :62@P :61@P :61@N1 out data/dihedral_530_529.dat
dihedral dh529_528 :61@N1 :61@P :60@P :60@N3 out data/dihedral_529_528.dat
dihedral dh528_527 :60@N3 :60@P :59@P :59@N1 out data/dihedral_528_527.dat
dihedral dh527_526 :59@N1 :59@P :58@P :58@N3 out data/dihedral_527_526.dat
""".format(struct_name)

    f = open("{}cpptraj_analysis.in".format(directory), "w")
    f.write(script_text)
    f.close()

def make_cpptraj_sh(struct_name, directory):
    script_text = """
#!/bin/bash
#BSUB -q amber128
#BSUB -n 1
#BSUB -J GPU_/home/weirlab/MDfiles/{0}_CPPTRAJ
#BSUB -o out
#BSUB -e error

# This script runs cpptraj
cpptraj -i cpptraj_analysis.in > cpptraj.log
""".format(struct_name.upper())
    f = open("{}run_cpptraj.sh".format(directory), "w")
    f.write(script_text)
    f.close()


if __name__ == "__main__":
    struct_name = "5jup"
    neutral_runs = glob.glob("NEUTRAL/*/")

    for run_dir in neutral_runs:
        # Checks to see if a data directory exists for cpptraj
        if not os.path.exists("{}/data/".format(run_dir)):
            os.makedirs("{}/data/".format(run_dir))

        make_cpptraj_in(struct_name, run_dir)
        make_cpptraj_sh(struct_name, run_dir)
