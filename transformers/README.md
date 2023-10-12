## Build

```shell
apptainer build --fakeroot nvidia_pytorch.sif ../nvidia_pytorch/nvidia_pytorch.def
apptainer build --fakeroot transformers.sif transformers.def
```

## Run

```shell
apptainer exec --nv transformers.sif python -c "import transformers"
```
