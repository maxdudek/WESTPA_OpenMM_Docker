FROM continuumio/anaconda

WORKDIR /home/test

RUN apt-get clean all
RUN apt-get update
RUN apt-get dist-upgrade -y
# and optionally
# apt-get autoremove


# Get GCC
RUN apt-get install -y g++ --fix-missing
# Get MDTraj
RUN pip install mdtraj
# Get OpenMM
RUN conda install -c omnia openmm
# Install WESTPA 
RUN git clone https://github.com/westpa/westpa.git
# Install vim
RUN apt-get install -y vim
# Install workshop tutorial
#RUN git clone https://github.com/ASinanSaglam/WESTPA_Workshop_2018_Saglam.git
#RUN mv WESTPA_Workshop_2018_Saglam /home/test/westpa/lib/examples
EXPOSE 8888

WORKDIR /home/test/westpa
RUN /home/test/westpa/setup.sh
#WORKDIR /home/test/westpa/lib/examples/WESTPA_Workshop_2018_Saglam
