#!/bin/bash
#SBATCH -A p32234              # Allocation
#SBATCH -p gengpu
#SBATCH --gres=gpu:1
#SBATCH -t 01:00:00             # Walltime/duration of the job
#SBATCH -N 1                    # Number of Nodes
#SBATCH --mem=64G               # Memory per node in GB needed for a job. Also see --mem-per-cpu
#SBATCH --ntasks-per-node=1     # Number of Cores (Processors)
#SBATCH --mail-user=aerith.netzer@northwestern.edu

cd ..
make extractcompanynames
