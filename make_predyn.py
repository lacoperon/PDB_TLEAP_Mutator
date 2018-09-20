def generate_predyn_sh(struct_name):

    script_text = """
#!/bin/bash
#################### BSUB LINES TO CONFIGURE SCHEDULING OF JOB
#BSUB -q amber128
#BSUB -n 1
#BSUB -R "rusage[gpu=1:mem=12288],span[hosts=1]"
#BSUB -J GPU_{1}_GC_PREDYN
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
#cd


## AMBER we need to recreate env, /home/apps/amber/12cpu-only is already set
export PATH=/share/apps/CENTOS6/python/2.7.9/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/CENTOS6/python/2.7.9/lib:$LD_LIBRARY_PATH
source /usr/local/amber16/amber.sh

# commands to run calculations go here.


################ Start job ##########################
# First clean out any diagnostic files from a previous run in this dir
if [ -f temp.out ]; then
     rm temp.out
fi
if [ -f time.log ]; then
     rm time.log
fi
if [ -f err ]; then
     rm err

fi
if [ -f out ]; then
     rm out
fi
if [ -f mdinfo ]; then
     rm mdinfo
fi
if [ -f logfile ]; then
     rm logfile
fi

################################### MD EQUILIBRATION STEPS ###################################
echo "MD PREDYNAMICS starting at " >> time.log
date >> time.log

############## Your Job Goes Here ############################
#lava.mvapich2.wrapper # OLD for Amber12

n78.mpich3.wrapper pmemd.cuda.MPI -O -i predyn.in -p ../TLEAP/{0}_gc_wat.prmtop -c ../EQUIL/{1}_gc_equil.rst -r {1}_gc_predyn.rst -ref ../EQUIL/{1}_gc_equil.rst -o 5JUP_GC_predyn.out

/share/apps/CENTOS6/amber/amber16/bin/ambpdb -p ../TLEAP/{0}_gc_wat.prmtop -c {1}_gc_predyn.rst > {1}_gc_predyn.pdb

echo "predynamics predyn_{1}_GC is complete. View {1}_GC_predyn.pdb with PyMol." | mailx -s "predyn_{1}_GC" ejwilliams@wesleyan.edu
""".format(struct_name, struct_name.upper())

    f = open("PREDYN/run_predyn.sh", "w")
    f.write(script_text)
    f.close()

def generate_predyn_in():
    input_text = """
100ps predynamics step (PREDYN -- 'equil part II')
 &cntrl
  imin     = 0,    !no minimization
  ntx      = 5,    !AMBER 16: Coordinates & Velocities are read
  irest    = 1,    !Flag to restart simulation (1, as ntx=5)
  ntpr     = 5000, !print energy info every `ntpr` steps
  ntwr     = 50000,!rewrite rst file every `ntwr` steps
  ntwx     = 1000, !write coord to trj every `ntwx` steps
  ntf      = 2,    !2 bond interactions involving H omitted ???
  ntc      = 2,    !SHAKE 2 Hbonds constrained, 1 turn off for minimization
  cut      = 8.0,  !non-bond cutoff of 8A
  ntb      = 2,    !2 periodic boundaries for constant pressure
  nstlim   = 50000,!number of MD steps to be performed
  dt       = 0.002,!time step in psec
  tempi    = 0.0,  !initial temperature
  temp0    = 300,  !ref temperature
  ntt      = 3,    !1 constant temperature 3 Langevin dynamics set ig ***
  gamma_ln = 1.0,  !collision freq when ntt=3, 0 default **
  ntp      = 1,    !constant pressure dynamics
  pres0    = 1.0,  !reference pressure 1
  taup     = 5.0,  !time constant for pressure
  nmropt   = 1,    !1 nmr restraints and weight changes will be read
  ioutfm   = 1,    !binary trajectory flag (we want 1 because smaller trj)
  ntr      = 1,    !flag for restraining atoms in mask (we want 1 because onion shell)
  restraint_wt = 20.0, ! restraint weight in kcal/mol Asquared
  restraintmask=':1-5,11-17,22-33,35,39-41,73-95,98-101,108-126,130-132,139-146,153-162,165-166,170-171,184-187,204-215,227-242,252-265,269-312,330-343,350-360,372-377,379-444,451-479,494-495',
  /
 &end
 &wt
  type='END',
 &end

"""

    f = open("PREDYN/predyn.in", 'w')
    f.write(input_text)
    f.close()

if __name__ == "__main__":


    if not os.path.exists("PREDYN/"):
        print("Making PREDYN directory")
        os.makedirs("PREDYN/")

    generate_predyn_sh("5jup")
    generate_predyn_in()
