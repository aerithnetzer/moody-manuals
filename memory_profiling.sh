#!/bin/bash
#SBATCH -A p32234              # Allocation
#SBATCH -p gengpu
#SBATCH --gres=gpu:1
#SBATCH -t 01:00:00             # Walltime/duration of the job
#SBATCH -N 1                    # Number of Nodes
#SBATCH --mem=128G               # Memory per node in GB needed for a job. Also see --mem-per-cpu
#SBATCH --ntasks-per-node=2     # Number of Cores (Processors)
#SBATCH --mail-user=aerith.netzer@northwestern.edu

export NUM_WORKERS = 4
uv run marker_single output.pdf --output_dir memory_profile
