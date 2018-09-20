'''
Elliot Williams
20th September 2018
make_emin.py

This script creates the correct script (.sh) files for AMBER 16, running
energy minimization for our 5JU*_GC Korostelev N1 subsystem.

The input files [`emin1.in`, ..., `emin11.in`] should be manually copied in.

All generated files will live within the `EMIN` subdirectory
'''

def generate_sh(struct_name):

    script_text = """
    #!/bin/bash
    #####PTT INITIALIZATION VARIABLES###
    #BSUB -q amber128
    #BSUB -n 1
    #BSUB -J /home/weirlab/MDfiles/{1}
    #BSUB -o out
    #BSUB -e err


    # env
    export PATH=/home/apps/amber/12cpu-only/bin:$PATH
    export LD_LIBRARY_PATH=/home/apps/amber/12cpu-only/lib:/home/apps/amber/12cpu-only/lib64:$LD_LIBRARY_PATH
    export PATH=/share/apps/openmpi/1.4.4+intel-12/bin:$PATH
    export LD_LIBRARY_PATH=/share/apps/openmpi/1.4.4+intel-12/lib:$LD_LIBRARY_PATH
    which sander.MPI mpicc

    # commands to run calculations go here.  Be sure to have all your input scripts ready to go.


    sander.MPI -O -i emin1.in -p ../TLEAP/{0}_wat.prmtop -c ../TLEAP/{0}_wat.rst -r {1}_wat_emin1.rst -ref ../TLEAP/{0}_wat.rst -o {1}_wat_emin1.out
    sander.MPI -O -i emin2.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin1.rst -r {1}_wat_emin2.rst -ref {1}_wat_emin1.rst -o {1}_wat_emin2.out
    sander.MPI -O -i emin3.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin2.rst -r {1}_wat_emin3.rst -ref {1}_wat_emin2.rst -o {1}_wat_emin3.out
    sander.MPI -O -i emin4.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin3.rst -r {1}_wat_emin4.rst -ref {1}_wat_emin3.rst -o {1}_wat_emin4.out
    sander.MPI -O -i emin5.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin4.rst -r {1}_wat_emin5.rst -ref {1}_wat_emin4.rst -o {1}_wat_emin5.out
    sander.MPI -O -i emin6.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin5.rst -r {1}_wat_emin6.rst -ref {1}_wat_emin5.rst -o {1}_wat_emin6.out
    sander.MPI -O -i emin7.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin6.rst -r {1}_wat_emin7.rst -ref {1}_wat_emin6.rst -o {1}_wat_emin7.out
    sander.MPI -O -i emin8.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin7.rst -r {1}_wat_emin8.rst -ref {1}_wat_emin7.rst -o {1}_wat_emin8.out
    sander.MPI -O -i emin9.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin8.rst -r {1}_wat_emin9.rst -ref {1}_wat_emin8.rst -o {1}_wat_emin9.out
    sander.MPI -O -i emin10.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin9.rst -r {1}_wat_emin10.rst -ref {1}_wat_emin9.rst -o {1}_wat_emin10.out
    sander.MPI -O -i emin11.in -p ../TLEAP/{0}_wat.prmtop -c {1}_wat_emin10.rst -r {1}_wat_emin11.rst -ref {1}_wat_emin10.rst -o {1}_wat_emin11.out
    """.format(struct_name, struct_name.upper())

    f = open("EMIN/run_emin.sh", "w")
    f.write(script_text)

if __name__ == "__main__":
    if not os.path.exists("EMIN/"):
        print("Making EMIN directory; remember to copy in the `emin*.in` files")
        os.makedirs("EMIN/")

    generate_sh("5jup_gc")
