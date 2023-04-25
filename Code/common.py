from os import path
from sys import argv

# If argv > 1, we are using the command line.
# Otherwise, we are in the interpreter.

if len( argv) > 1:
  import Code.params.cl    as imp
else:
  import Code.params.fixed as imp

subsample = imp.subsample
vintage   = imp.vintage

# PITFALL: These might not look worth defining, but they are!
# That's because we might bifurcate the input and output paths further.
# Currently they bifurcate based only on `vintage`.
# Bifurcation those paths is painful if it requires
# updating every site that uses those paths.
indata  = path.join ( "data", str(vintage) )
outdata = path.join ( "data", str(vintage) )
