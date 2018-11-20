#!/usr/bin/env python
import numpy, westpa
import mdtraj as md

def coord_loader(fieldname, coord_filename, segment, single_point=False):
    """
    Loads and stores coordinates

    **Arguments:**
        :*fieldname*:      Key at which to store dataset (should be 'coord')
        :*coord_filename*: Temporary file from which to load coordinates (a trajectory file)
        :*segment*:        WEST segment
        :*single_point*:   Data to be stored for a single frame
                           (should always be false)
    """
    topFile = "prep/nacl.parm7" # topology file

    # Create a trajectory object with MDTraj
    traj = md.load_netcdf(coord_filename, top=topFile)

    # Save the coordinats of Na and Cl as a list
    coord_data = []

    for frame in traj.xyz:
        coord_data.append([frame[0].tolist(), frame[1].tolist()])

    # turn list into numpy array
    coords = numpy.asarray(coord_data)

    # Save to hdf5
    segment.data[fieldname] = coords[...]
