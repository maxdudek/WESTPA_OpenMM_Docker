# WESPTA OpenMM Docker Image

## Components included in the Docker Image
* Anaconda (Python 2.7): A [pre-built image](https://hub.docker.com/r/continuumio/anaconda/) which is used as a base. Python is used to run all of the components of the simulation, and the anaconda distribution is used to install OpenMM and MDTraj. 
* [WESTPA](https://github.com/westpa/westpa): a package for constructing and running stochastic simulations using the "weighted ensemble" approach.
* [OpenMM](http://openmm.org/): A molecular dynamics engine with Python support
* [MDTraj](http://mdtraj.org/): A python-based molecular dynamics toolkit, used to calculate the progress coordinate for our simulation.
* [ParmEd](https://github.com/ParmEd/ParmEd): A tool for editing topology files, and used to create restart files with OpenMM.
* GCC: Necessary for the installation of MDTraj
* Vim: A UNIX text editor
* The files in this repository: used to set up and run the simulation

## Preparing for the simulation

This tutorial is based off of the [Na Cl Association with AMBER 16](https://github.com/westpa/westpa/wiki/Na--Cl--Association-with-AMBER-16) WESTPA tutorial. Familiarity with this tutorial and basic WESTPA operation is a prerequisite. 

This tutorial uses the OpenMM dynamics engine instead of AMBER, though OpenMM includes support for AMBER input files, and so the provided coordinate and topology files are the same as in the AMBER tutorial. The system has already been solvated using the procedure specified in that tutorial.

Instead of using CPPTRAJ to calculate the progress coordinate, this tutorial uses MDTraj. The script `pcoord_loader.py` is specified in `west.cfg` as the function which calculates the progress coordinate. The script `runDynamics.py` is called by `westpa_scripts/runsegs.sh` to run OpenMM dynamics for one segment. Besides these modifications to work with OpenMM, the flow of the simulation is similar to the AMBER tutorial. 


## Building the Docker Image

The only file you'll need to download from this repository is docker/Dockerfile

First, ensure that the docker daemon is running. It can be started with:
```
sudo dockerd
```

From the `docker/` directory, build the docker image:
```
sudo docker build -t westpa-openmm ./
```

Docker will build an image and install all of the necessary components. When the image is built for the first time, Docker will cache the components, and if the image is built again that cache will be used. The consequence of this is that any updates to the components will not take effect even if the image is built again. If you want to re-build the image without the cache, use the `--no-cache` option:

```
sudo docker build --no-cache -t westpa-openmm ./
```
Entering a `tmux` session now is recommended, so that the session can be detached and reattached to later.
 
Run the image and start an interactive bash session in the container:
```
sudo docker run -it westpa-openmm /bin/bash
```

The image will start in the simulation directory.

---
NOTE: If at any time you wish to exit this session, use the `exit` command. However, note that any operations done to the container will be erased the next time you run the image. To save the container to a new image, so that it can be run again with changes, see below.

---

## Prepping and Running the Simulation

To run an equilibration and minimize the energy of the system, run the python script prep.py:

```
python prep/prep.py
```

This may take a few minutes.

Next, initialize the simulation:
```
./init.sh
```

And run the simulation:
```
./run.sh
```

## Saving the container to a new image

To save a container as a new image, you will need to know the ID of the container. From **outside the docker bash session** (tmux is useful here) use  `sudo docker ps` to get a readout of all running containers. 

Then commit a new image with a specified name:

```
sudo docker commit <container_id> new_image_name
```

You will then be able to run a container with this new image just like before:

```
sudo docker run -it new_image_name /bin/bash
```