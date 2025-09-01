#!/bin/bash
#SBATCH --job-name=velo_sweep
#SBATCH --output=logs/array_%A_%a.out
#SBATCH --error=logs/array_%A_%a.err
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
# TODO: EDIT THIS RANGE to match number of rows in params.csv (0..N-1)
# Count the rows in your params.csv file and set the array range accordingly
# For example, if params.csv has 10 rows, use --array=0-9
#SBATCH --array=0-4

set -euo pipefail

# TODO: Load required modules for your HPC system
# Examples:
# module purge || true
# module load python/3.11
# module load apptainer  # if using containers

# TODO: Create necessary directories
# mkdir -p logs results

# TODO: Set up environment variables
# ROW_IDX=${SLURM_ARRAY_TASK_ID}  # This gets the current array task ID
# BASE_SEED=0  # Base seed for reproducibility

# TODO: Choose one of the execution methods below:

# Method 1: Bare-metal execution (direct Python)
# Uncomment and modify the following line:
# python run_one.py --params params.csv --row-index ${ROW_IDX} --out-dir results --base-seed ${BASE_SEED}

# Method 2: Container execution (recommended for HPC)
# Uncomment and modify the following lines:
# apptainer exec --bind "$PWD:$PWD" containers/velo.sif \
#   python 4_cluster_slurm/run_one.py --params 4_cluster_slurm/params.csv \
#   --row-index ${ROW_IDX} --out-dir 4_cluster_slurm/results --base-seed ${BASE_SEED}

# Method 3: Virtual environment execution
# Uncomment and modify the following lines:
# source /path/to/your/venv/bin/activate
# python run_one.py --params params.csv --row-index ${ROW_IDX} --out-dir results --base-seed ${BASE_SEED}

# TODO: Add any post-processing or cleanup commands if needed
