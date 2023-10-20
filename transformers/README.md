## Build
This container is built on top of the `nvidia_pytorch` container:

```shell
apptainer build --fakeroot nvidia_pytorch.sif ../nvidia_pytorch/nvidia_pytorch.def
apptainer build --fakeroot transformers.sif transformers.def
```

## Run
```shell
apptainer exec --nv transformers.sif python -c "import transformers"
```

## Examples
The `example.py` and `example.slurm` scripts showcase how to perform a multi-node multi-gpu training with Hugging Face's transformers library.
Here we will fine-tune a distilled version of GPT2 on a small Shakespear dataset, using 2 nodes with 4 GPUs each.

First, get the Shakespear data:
```shell
wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt .
```

The transformers `Trainer` (together with Accelerate) and the `torchrun` command basically automates everything.
We can use the same python script to run a single-device training on our laptop/machine, or a multi-device training on our SLURM cluster.

To run the example locally on our machine:
```shell
apptainer exec --nv transformers.sif python example.py
```

To run a multi-node multi-GPU training on our SLURM cluster we just need to specify the resources we want to use in the SLURM script:
```shell
#SBATCH --nodes=2  # <- Number of nodes we want to use for the training
#SBATCH --tasks-per-node=1  # <- Has to be 1, since torchrun takes care of spawning the processes for each GPU
#SBATCH --gres=gpu:a100:4  # <- Number of GPUs you want to use per node, here 4
```

Send the job to the queue:
```shell
sbatch example.slurm
```

Since we bind the container's home folder to the current working dir (`-B .:"$HOME"`), the pretrained model and the dataset preprocessing will be cached in the `./.cache` folder.
After the training, you can find the fine-tuned model in the `./model` folder.

## Notes
- Be aware of HuggingFace's caching mechanisms when running a multi-gpu training! Maybe download the models/datasets first and instantiate the respective classes with the files directly to avoid concurrent downloads of the same files.
