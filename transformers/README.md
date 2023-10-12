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
**TODO:** Provide an example of how to run a distributed transformer training (example python and slurm script)
