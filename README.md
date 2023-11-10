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

## Local-to-HPC Workflow

A nice workflow to develop a python library locally and deploy it on our HPO systems (sharing exactly the same environment) is to use the [*sandbox* feature](https://apptainer.org/docs/user/main/build_a_container.html#sandbox) of Apptainer.

We are still investigating if someting similar is possible with `Docker` (please let us know if you find a way :) ).

### 1. Create a definition file

In the root directory of your library (repository) create a *definition* `*.def` file.
This definition file should reflect your environment in which you want your library to develop and use.

You can leverage base environments, such as docker images on DockerHub, or existing apptainers.

### 2. Build the sandbox

Build the sandbox (container in a directory) instead of the default SIF format:

```shell
apptainer build --fakeroot --sandbox my_container my_container.def
```

### 3. Install your library in the sandbox

Now we can add our library that we develop to the sandbox environment and install it in [`editable`](https://setuptools.pypa.io/en/latest/userguide/development_mode.html) mode:

```shell
apptainer exec --writable my_container python -m pip install -e .
```

### 4. Point your IDE's interpreter to the sandbox

You should be able to point the interpreter of your IDE (VSC, PyCharm, etc.) to the python executable inside the sandbox folder.

### 5. Add your developed library to the my_container.def file

While in principle you could build a SIF container directly from your sandbox, it is better to modify your *definition* `*.def` file to include your library/package.
In this way, your container is fully reproducible using only the definition file. 

### 6. Build your *.sif apptainer, deploy on our HPC systems

Once you built the SIF container, you can copy it to our HPC systems and use it there.

```shell
apptainer build --fakeroot my_container.sif my_container.def
```

## Running containers

**TODO:**
- how to run the containers on our SLURM cluster
- mention important flags, like `--nv` for example


