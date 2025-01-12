#!/bin/bash
#SBATCH --account=b1094
#SBATCH --partition=ciera-std
#SBATCH --job-name=test
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=52
#SBATCH --time=24:00:00
#SBATCH --output=test9b.log
#SBATCH --constraint="[quest9|quest10|quest11|quest12]"


source ~/.bashrc
dedalus3
export OMP_NUM_THREADS=1
mpirun -np 96 python3 rbc9b.py

echo "done"
