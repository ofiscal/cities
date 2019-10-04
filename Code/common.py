from sys import argv

# If argv > 1, we are using the command line.
# Otherwise, we are in the interpreter.

if len( argv) > 1:
  import Code.params.cl    as imp
else:
  import Code.params.fixed as imp

subsample = imp.subsample
