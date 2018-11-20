from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
import sys
import numpy
import os
from mdtraj.reporters import NetCDFReporter
from parmed.openmm.reporters import RestartReporter

# Get arguments from the command line
# The call to this script in runseg.sh is:
# python runDynamics.py nacl.parm7 parent.rst seg.rst seg.nc seg.log
topologyFile = sys.argv[1]
parentRestartFile = sys.argv[2]
restartFile = sys.argv[3]
trajectoryFile = sys.argv[4]
logFile = sys.argv[5]

# Declare simulation constants
TAU = 5.0*picoseconds                   # The length of every iteration
#TAU = 200.0*femtoseconds                # Test length
TIMESTEP = 2.0*femtoseconds             # The length of every frame of the simulation
TIMESTEPS = int(round(TAU / TIMESTEP))  # The number of frames per iteration (5000 / 2 is 2500)

# Load the topology and coordinate files into OpenMM using AMBER files
prmtop = AmberPrmtopFile(topologyFile)
inpcrd = AmberInpcrdFile(parentRestartFile)

# Create the OpenMM simulation
system = prmtop.createSystem(
    #nonbondedMethod=PME,
    nonbondedCutoff=1*nanometer,
    constraints=HBonds)
# LangevinIntegrator(temperature, frictionCoefficient, timeStepLength)
integrator = LangevinIntegrator(300*kelvin, 0.5/picoseconds, TIMESTEP)
simulation = Simulation(prmtop.topology, system, integrator)
simulation.context.setPositions(inpcrd.positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

# Create a reporter which will output the trajectory (seg.nc) file
# Every 50 frames, add the coordinates to the trajectory file output
# After 2500 frames, coordinates will be added 50 times
# This is why pcoord_len (progress coordinate length) is 50, because
# the pccord will be an array of length 50: one distance for every frame
simulation.reporters.append(NetCDFReporter(trajectoryFile, 50))

#Create restart reporter which will output a .rst file
#RestartReporter(restartFile, numberOfSteps, numberOfAtoms, usesPeriodicBoundaryConditions)
simulation.reporters.append(RestartReporter(restartFile, TIMESTEPS, prmtop.topology.getNumAtoms()))

#Create log reporter which will output seg.log
#TODO: What data should this report?
simulation.reporters.append(StateDataReporter(logFile, TIMESTEPS, step=True, potentialEnergy=True, temperature=True))

#Run the dynamics
simulation.step(TIMESTEPS)

# Rename the restart file, because the parmEd reporter adds an extension
os.rename(restartFile+"."+str(TIMESTEPS), restartFile)
