from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
from parmed.openmm.reporters import RestartReporter
from mdtraj.reporters import NetCDFReporter
import os

# Load the topology and coordinate files into OpenMM using AMBER files
prmtop = AmberPrmtopFile('nacl.parm7')
inpcrd = AmberInpcrdFile('nacl.rst')

# Create the system
system = prmtop.createSystem(
    #nonbondedMethod=PME,
    nonbondedCutoff=1*nanometer,
    constraints=HBonds)
integrator = LangevinIntegrator(300*kelvin, 0.5/picoseconds, 2.0*femtoseconds)
simulation = Simulation(prmtop.topology, system, integrator)
simulation.context.setPositions(inpcrd.positions)
if inpcrd.boxVectors is not None:
    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)

# Minimize energy
simulation.minimizeEnergy()

# Create a RestartReporter which will output the restart file
simulation.reporters.append(RestartReporter('nacl_eq.rst', 1, prmtop.topology.getNumAtoms()))

# Create a NetCDF reporter which outputs a trajectory file
# This is used to calculate the initial progress coordinate in get_pcoord.sh
simulation.reporters.append(NetCDFReporter('nacl_eq.nc', 1))

# Run the simulation for a single frame so that files can be outputed
simulation.step(1)

# Rename the restart file, because the parmEd reporter adds an extension
os.rename('nacl_eq.rst.1', 'nacl_eq.rst')
