#!/bin/bash
#SBATCH --account=b1094
#SBATCH --partition=ciera-std
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=04:00:00
#SBATCH --output=test8b.log

source ~/.bashrc
dedalus3
export OMP_NUM_THREADS=1
mpirun -np 16 python3 rbc8b.py

echo "done"
