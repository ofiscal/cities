from os import path
from sys import argv
#
from Code.params.cl import vintage_universe

# If argv > 1, we are using the command line.
# Otherwise, we are in the interpreter.

if len( argv) > 1:
  import Code.params.cl    as imp
else:
  import Code.params.fixed as imp


subsample = imp.subsample
vintage   = imp.vintage

first_year = 2013
if   vintage == 2019: last_year = 2018
elif vintage == 2023: last_year = 2021
else: raise ValueError ( "vintage not in ", vintage_universe )

# PITFALL: These might not look worth defining, but they are!
# That's because we might bifurcate the input and output paths further.
# Currently they bifurcate based only on `vintage`.
# Bifurcation those paths is painful if it requires
# updating every site that uses those paths.
indata  = path.join ( "data",   str(vintage) )
outdata = path.join ( "output", str(vintage) )
