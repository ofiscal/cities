# PITFALL: Don't include this in the Makefile.

import argparse, sys
#
import Code.params.cl_arg_universe as clau


parser = argparse.ArgumentParser ()
parser.add_argument (
  "--subsample",
  help = ( "Inverse of sample size. Should take a value in "
           + str ( clau.subsample_universe ) ) )
parser.add_argument (
  "--vintage",
  help = ( "Source year. Should take a value in "
           + str ( clau.vintage_universe ) ) )
args = parser.parse_args ()

subsample = int( args.subsample )
if not subsample in clau.subsample_universe:
  raise ValueError("subsample not in ", clau.subsample_universe)

vintage   = int( args.vintage )
if not vintage in clau.vintage_universe:
  raise ValueError("vintage not in ", clau.vintage_universe)
