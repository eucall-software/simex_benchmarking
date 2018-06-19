#!/bin/bash --login

### Batch job script
### Scheduler: slurm
### Author: Carsten Fortmann-Grote <carsten.grote@xfel.eu>


#SBATCH --partition=exfel-spb
#SBATCH --constraint=INTEL
#SBATCH --time=7-0
#SBATCH --nodes=3
#SBATCH --job-name singfel-%j
#SBATCH --output singfel-%j.log
#SBATCH --mail-type ALL
#SBATCH --mail-user carsten.grote@desy.de

module load simex.maxwell

export SIMEX_VERBOSE=MPI
export SIMEX_NCORES=54
export SIMEX_NNODES=3

python singfel.py
