#!/bin/bash
#SBATCH -A p32234              # Allocation
#SBATCH -p gengpu
#SBATCH --gres=gpu:1
#SBATCH -t 16:00:00             # Walltime/duration of the job
#SBATCH -N 1                    # Number of Nodes
#SBATCH --mem=512G               # Memory per node in GB needed for a job. Also see --mem-per-cpu
#SBATCH --ntasks-per-node=1     # Number of Cores (Processors)
#SBATCH --mail-user=aerith.netzer@northwestern.edu

uv run chandra ./output.pdf ./chandra --method hf --batch-size 8
