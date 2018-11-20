# WESPTA OpenMM Docker Image

## Components included in the Docker Image
* Anaconda (Python 2.7): A [pre-built image](https://hub.docker.com/r/continuumio/anaconda/) which is used as a base. Python is used to run all of the components of the simulation, and the anaconda distribution is used to install OpenMM and MDTraj. 
* [WESTPA](https://github.com/westpa/westpa): a package for constructing and running stochastic simulations using the "weighted ensemble" approach.
* [OpenMM](http://openmm.org/): A molecular dynamics engine with Python support
* [MDTraj](http://mdtraj.org/): A python-based molecular dynamics toolkit, used to calculate the progress coordinate for our simulation.
* GCC: Necessary for the installation of MDTraj
* Vim: A UNIX text editor
* The files in this repository: used to set up and run the simulation

## Building the Docker Image

The only file you'll need to download is docker/Dockerfile

First, ensure that the docker daemon is running. It can be started with:
`sudo dockerd`

From the `docker/` directory, build the docker image:
`sudo docker build -t westpa-openmm ./`

Docker will build an image and install all of the necessary components. 

To start an interactive bash session in the image created:
`sudo docker run -it westpa-openmm /bin/bash` 

To set the environment variable $WEST_ROOT, run the following from the westpa/ directory:
`source westpa.sh`

Now enter the simulation directory:
`cd lib/examples/WESTPA_OpenMM_Docker/`

Initialize the simulation:
`./init.sh`

Run the simulation:
`./run.sh`