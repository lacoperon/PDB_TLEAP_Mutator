def generate_heat_sh(struct_name):

    script_text = """#!/bin/bash
#BSUB -q amber128
#BSUB -n 1
#BSUB -R "rusage[gpu=1:mem=12288],span[hosts=1]"
#BSUB -J GPU_{1}_HEAT
#BSUB -o out
#BSUB -e err

## leave sufficient time between job submissions (30-60 secs)
## the number of GPUs allocated matches -n value automatically
## always reserve GPU (gpu=1), setting this to 0 is a cpu job only
## reserve 6144 MB (5 GB + 20%) memory per GPU
## run all processes (1<=n<=4)) on same node (hosts=1).


# cuda 8 & mpich *NEW* for AMBER16
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/mpich-3.1.4/bin:/home/apps/amber/12cpu-only/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/mpich-3.1.4/lib:$LD_LIBRARY_PATH

# unique job scratch dirs *NEW* for AMBER16
MYSANSCRATCH=/sanscratch/
MYLOCALSCRATCH=/localscratch/
export MYSANSCRATCH MYLOCALSCRATCH

## AMBER we need to recreate env, /home/apps/amber/12cpu-only is already set
export PATH=/share/apps/CENTOS6/python/2.7.9/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/CENTOS6/python/2.7.9/lib:$LD_LIBRARY_PATH
source /usr/local/amber16/amber.sh

# commands to run calculations go here.

# MD sim: Heating
n78.mpich3.wrapper pmemd.cuda.MPI -O -i heat.in -o {0}_gc_heat.out -p ../TLEAP/{0}_gc_wat.prmtop -c ../EMIN/{1}_GC_wat_emin11.rst -r {1}_gc_heat.rst -ref ../EMIN/{1}_GC_wat_emin11.rst

# make pdb snapshot
/share/apps/CENTOS6/amber/amber16/bin/ambpdb -p ../TLEAP/{0}_gc_wat.prmtop -c {1}_gc_heat.rst > {0}_gc_heat.pdb

echo 'Your heating job heat_{1} is complete.' | mailx -s "heat_{1}" ejwilliams@wesleyan.edu
# Please make sure you're meaning to send me emails if you do
""".format(struct_name, struct_name.upper())

    f = open("HEAT/run_heat.sh", "w")
    f.write(script_text)
    f.close()

def generate_heat_in():
    input_text = """
heating: MD with restraint on molecule
 &cntrl
  imin=0,
  irest=0,
  ntx=1,
  ntb=1,
  cut=10,
  ntr=1, restraintmask=':1 - 495',restraint_wt=20.0,
  ntc=2, ntf=2,
  tempi=0.0,
  temp0=300.0,
  ntt=3, gamma_ln=1.0,
  nstlim=10000, dt=0.002,
  ntpr=1000, ntwx=1000, ntwr=10000
 /
"""

    f = open("HEAT/heat.in", 'w')
    f.write(input_text)
    f.close()

if __name__ == "__main__":
    generate_heat_sh("5jup")
    generate_heat_in()
