## Build

```shell
apptainer build --fakeroot nvidia_pytorch.sif nvidia_pytorch.def
```

## Run

```shell
apptainer exec --nv nvidia_pytorch.sif python -c "import torch; print(torch.cuda.device_count())"
```