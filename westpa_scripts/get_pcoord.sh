#!/bin/bash
#
# get_pcoord.sh
#
# This script is run when calculating initial progress coordinates for new 
# initial states (istates).  This script is NOT run for calculating the progress
# coordinates of most trajectory segments; that is instead the job of runseg.sh.

# If we are debugging, output a lot of extra information.
if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

# Make sure we are in the correct directory
cd $WEST_SIM_ROOT

# Allow pcoord_loader.pcoord_loader (specified in west.cfg) to calculate the progress coordinate
cp prep/nacl_eq.nc $WEST_PCOORD_RETURN


if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi
