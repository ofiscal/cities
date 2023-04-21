# PITFALL: Don't include this in the Makefile.

import argparse, sys


parser = argparse.ArgumentParser ()
parser.add_argument ( "--subsample",
                      help = "Inverse of sample size: 1, 10, 100, or 1000.")
parser.add_argument ( "--vintage",
                      help = "Source year (2019 or 2023).")
args = parser.parse_args ()

subsample = int( args.subsample )
vintage   = int( args.vintage )
