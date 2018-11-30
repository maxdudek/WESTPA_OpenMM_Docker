import mdtraj as md
import numpy, westpa

def pcoord_loader(fieldname, pcoord_return_filename, segment, single_point=False):
    # This function is specified in west.cfg under executable/datasets as the
    # function which calculates and returns the progress coordinate (pcoord)

    # fieldname: should always be 'pcoord' for this function, as it's the pcoord.

    # pcoord_return_filename: a string containing the filename of whatever is copied/piped
    # into $WEST_PCOORD_RETURN. In this case, it will be a trajectory file
    # which we are using to calculate the distance between Na and Cl.

    # segment: the segment object itself.  We'll be replacing
    # segment.pcoord with the progress coordinate (distance) we calculate here.

    # single_point: whether we're evaluating a basis/initial state or not.
    # During dynamics, it's false, which means our pcoord should be a numpy array
    # shaped as ndim/pcoord_length, as defined in west.cfg
    # Otherwise, it's a numpy array with shape = ndim.

    # Lets us reference variables from WESTPA
    system = westpa.rc.get_system_driver()

    # Make sure that the fieldname argument is 'pcoord'
    assert fieldname == 'pcoord'

    # Locate the topology file
    topFile = 'prep/nacl.parm7'


    # Load the trajectory
    # Here the .load_netcdf() function is used to let MDTraj know to read it as a NetCDF file
    traj = md.load_netcdf(pcoord_return_filename, top=topFile)

    # Below we check to make sure the shape of the array is what WESTPA expects.
    # Here system.pcoord_ndim refers to the number of dimensions in the
    # progress coordinate, which in this case is 1.
    # system.pcoord_len refers to the number of times the trajectory coordinates
    # are saved during each iteration (50 in this case)

    # An array to store the distances between Na and Cl during each frame
    dist = []

    # traj.xyz = Cartesian coordinates of each atom in each simulation frame
    # np.ndarray, shape=(n_frames, n_atoms, 3)
    for frame in traj.xyz:
        coords1 = frame[0] # Coordinates of first atom
        coords2 = frame[1] # Coordinates of second atom

        # For debugging
        #print("Na and Cl coords:")
        #print(coords1)
        #print(coords2)

        # Calclulate the distance between Na and Cl
        # MDTraj uses nm, but WESTPA uses angstroms, so we multiply by 10 to correct
        dist.append(10*getDistance(coords1, coords2))
        #dist.append(10) # Testing

    dist = numpy.asarray(dist, dtype = numpy.float32)

    # for debugging
    #dist = numpy.ones((50,1), dtype=numpy.float32)


    # The check is different if we are checking a single point during initialization.
    # If single_point = True, then we only need the last value in the array.
    if single_point:
        dist = numpy.array(dist[-1]) # Get the last value in the array
        expected_shape = (system.pcoord_ndim,) # Expects a 1x1 array
        #Correct the shape if needed
        if dist.ndim == 0:
            dist.shape = (1,)

    # During dynamics, WESTPA expects a 2D array, with size (pcoord_len, pcoord_ndim)
    else:
        expected_shape = (system.pcoord_len, system.pcoord_ndim) # Expects a 50x1 array
        if dist.ndim == 1:
            dist.shape = (len(dist),1)

    # Send a debug message if the shape is different from what is expected
    if dist.shape != expected_shape:
        raise ValueError('progress coordinate data has incorrect shape {!r} [expected {!r}]'.format(dist.shape,
                                                                                                    expected_shape))
    # For debugging
    #print("pcoord:")
    #print(dist)

    # Send the calculated dist array to the segment object
    segment.pcoord = dist

def getDistance(coords1, coords2):
    """
    Takes two 3-element numpy arrays (xyz coordinates)
    and returns the distance between the two
    """
    x1 = coords1[0]
    y1 = coords1[1]
    z1 = coords1[2]

    x2 = coords2[0]
    y2 = coords2[1]
    z2 = coords2[2]





    return numpy.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
