# containers

Goal: compile definition files of containers for AI use cases.
Also provide documentation on how to use them on our HPC systems.

## Getting started
We use [Apptainer](https://apptainer.org/docs/user/main/index.html) to build/run containers on our HPC systems.
You will need a Linux system to run Apptainer natively on your machine, and it’s easiest to [install](https://apptainer.org/docs/user/main/quick_start.html) if you have root access.

But it is also easy to use or convert [docker images with Apptainer](https://apptainer.org/docs/user/main/docker_and_oci.html).

For a nice introduction to Apptainer on our HPC systems, have a look at the awesome [presentation by Michele](https://datashare.mpcdf.mpg.de/s/df4p3bMuWCF53Y3).
You can also browse [our documentation](https://docs.mpcdf.mpg.de/doc/computing/software/containers.html#apptainer).

## Building containers
Containers are built via a [definition file](https://apptainer.org/docs/user/latest/definition_files.html) and the `apptainer build` command.

In each folder of this repo you will find a definition `.def` file and a `README.md` that describes the exact build command.

## Running containers
**TODO:**
- how to run the containers on our SLURM cluster
- mention important flags, like `--nv` for example


