# PITFALL: Don't include this in the Makefile.

import argparse, sys


subsample_universe = [1,10,100,1000]
vintage_universe   = [2019,2023]

parser = argparse.ArgumentParser ()
parser.add_argument (
  "--subsample",
  help = ( "Inverse of sample size. Should take a value in "
           + str ( subsample_universe ) ) )
parser.add_argument (
  "--vintage",
  help = ( "Source year. Should take a value in "
           + str ( vintage_universe ) ) )
args = parser.parse_args ()

subsample = int( args.subsample )
if not subsample in subsample_universe:
  raise ValueError("subsample not in ", subsample_universe)

vintage   = int( args.vintage )
if not vintage in vintage_universe:
  raise ValueError("vintage not in ", vintage_universe)
