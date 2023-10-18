#!/bin/bash -l
#
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J transformers
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=36
#SBATCH --mem=0
#
#SBATCH --constraint="gpu"
#SBATCH --gres=gpu:a100:2
#
#SBATCH --mail-type=none
#SBATCH --mail-user=david.carreto.fidalgo@gmail.com
#
# Wall clock limit (max. is 24 hours):
#SBATCH --time=00:15:00

source /etc/profile.d/modules.sh
module purge
module load apptainer
#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=18


# For pinning threads correctly:
export OMP_PLACES=cores

nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory --format=csv -l 1 > nvidia_smi_monitoring.csv &
NVIDIASMI_PID=$!

srun apptainer exec --nv -B .:"$HOME" transformers.sif torchrun --standalone --nnodes=1 --nproc-per-node=2 train_agent.py

kill $NVIDIASMI_PID

