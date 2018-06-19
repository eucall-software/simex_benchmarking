#!/bin/bash --login

### Batch job script
### Scheduler: slurm
### Author: Carsten Fortmann-Grote <carsten.grote@xfel.eu>


#SBATCH --partition=exfel-spb
#SBATCH --constraint=INTEL
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --job-name gapd
#SBATCH --output gapd=%j.log
#SBATCH --mail-type ALL
#SBATCH --mail-user carsten.grote@desy.de

module load simex.maxwell


GAPD.cuda -i c60.gapd.in
