FROM continuumio/anaconda

WORKDIR /home/test

# Ensure integrity of files
RUN apt-get clean all
RUN apt-get update
RUN apt-get dist-upgrade -y

# Get GCC
RUN apt-get install -y g++ --fix-missing
# Get MDTraj
RUN pip install mdtraj
# Get OpenMM
RUN conda install -c omnia openmm
# Ensure than numpy and its components are up to date
RUN conda install libgfortran==1
RUN pip install --upgrade numpy
# Install ParmEd - used to create restart files with OpenMM
RUN git clone https://github.com/ParmEd/ParmEd.git
WORKDIR /home/test/ParmEd
RUN python setup.py install
# Install WESTPA 
WORKDIR /home/test
RUN git clone https://github.com/westpa/westpa.git
# Install vim
RUN apt-get install -y vim
# Install workshop tutorial
RUN git clone https://github.com/maxdudek/WESTPA_OpenMM_Docker.git
RUN mv WESTPA_OpenMM_Docker /home/test/westpa/lib/examples
EXPOSE 8888

WORKDIR /home/test/westpa

# Set WESTPA environment variables
RUN /home/test/westpa/setup.sh
ARG _WEST_ROOT=/home/test/westpa
ENV WEST_ROOT=$_WEST_ROOT
ARG _WEST_BIN=/home/test/westpa/bin
ENV WEST_BIN=$_WEST_BIN
ARG _WEST_PYTHON=/opt/conda/bin/python2.7
ENV WEST_PYTHON=$_WEST_PYTHON
ARG _PATH=$WEST_BIN:$PATH
ENV PATH=$_PATH

WORKDIR /home/test/westpa/lib/examples/WESTPA_OpenMM_Docker
