#!/bin/bash
#
# runseg.sh
#
# WESTPA runs this script for each trajectory segment. WESTPA supplies
# environment variables that are unique to each segment, such as:
#
#   WEST_CURRENT_SEG_DATA_REF: A path to where the current trajectory segment's
#       data will be stored. This will become "WEST_PARENT_DATA_REF" for any
#       child segments that spawn from this segment
#   WEST_PARENT_DATA_REF: A path to a file or directory containing data for the
#       parent segment.
#   WEST_CURRENT_SEG_INITPOINT_TYPE: Specifies whether this segment is starting
#       anew, or if this segment continues from where another segment left off.
#   WEST_RAND16: A random integer
#
# This script has the following three jobs:
#  1. Create a directory for the current trajectory segment, and set up the
#     directory for running pmemd/sander
#  2. Run the dynamics
#  3. Calculate the progress coordinates and return data to WESTPA


# If we are running in debug mode, then output a lot of extra information.
if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

######################## Set up for running the dynamics #######################

# Set up the directory where data for this segment will be stored.
cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

# Make a symbolic link to the topology file. This is not unique to each segment.
ln -sv $WEST_SIM_ROOT/prep/nacl.parm7 .

# Either continue an existing tractory, or start a new trajectory. In the
# latter case, we need to do a couple things differently, such as generating
# velocities.
#
# First, take care of the case that this segment is a continuation of another
# segment.  WESTPA provides the environment variable
# $WEST_CURRENT_SEG_INITPOINT_TYPE, and we check its value.
if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then

  # This trajectory segment will start off where its parent segment left off.
  # The "ln" command makes symbolic links to the parent segment's rst file.
  # This is preferable to copying the files, since it doesn't
  # require writing all the data again.
  ln -sv $WEST_PARENT_DATA_REF/seg.rst ./parent.rst

# Now take care of the case that the trajectory is starting anew.
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then

  # For a new segment, we only need to make a symbolic link to the .rst file.
  ln -sv $WEST_PARENT_DATA_REF ./parent.rst
fi


############################## Run the dynamics ################################
# Propagate segment using the OpenMM python script
python $WEST_SIM_ROOT/runDynamics.py nacl.parm7 parent.rst seg.rst seg.nc seg.log


########################## Calculate and return data ###########################
# Save the coordinates
# Copying the trajectory file here will allow the function coord_loader (in aux_functions.py)
# to save the coordinates to the h5 file. The file will be passed in to the function as
# the 'coord_filename' parameter. The function is specified
# as the coord loading function in west.cfg under executable/datasets
# cp seg.nc $WEST_COORD_RETURN

# Calculate the progress coordinate
# The progress coordinate is calculated and returned by the function pcoord_loader (in pcoord_loader.py)
# This function is specified in west.cfg under executable/datasets as the pcoord_loader
# Copying the file into this location allows it to be passed in to the function as the 'pcoord_return_filename' paramener
cp seg.nc $WEST_PCOORD_RETURN


# Clean up
rm -f $TEMP parent.rst nacl.parm7
