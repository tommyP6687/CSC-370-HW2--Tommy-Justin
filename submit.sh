#!/bin/bash

#SBATCH --mem 2g
#SBATCH --time=05:00:00

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=gipham@davidson.edu

# record start time
start=$(date +%s)
echo "Job started: $(date)"

python -u symbolic_regression.py

# record end time & print duration
end=$(date +%s)
elapsed=$((end - start))
echo "Job finished: $(date)"
printf "Total run time: %02d:%02d:%02d (hh:mm:ss)\n" $((elapsed/3600)) $((elapsed%3600/60)) $((elapsed%60))