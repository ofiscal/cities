from os import path
from sys import argv
#
from Code.params.cl_arg_universe import vintage_universe


# If argv > 1, we are using the command line.
# Otherwise, we are in the interpreter.

# PITFALL: Mypy flags the second import as an error, but it is not.
if len( argv) > 1:
  import Code.params.cl    as imp
else:
  import Code.params.fixed as imp


subsample = imp.subsample
vintage   = imp.vintage

first_year = 2013         # Data starts here.
if   vintage == 2019:
  admin_first_year = 2016 # Latest admin started office.
  last_year        = 2018 # Data ends here.
elif vintage       == 2023:
  admin_first_year = 2020 # Latest admin started office.
  last_year        = 2021 # Data ends here at the latest.
                          # (FOr most munis it ends earlier,
                          # in 2020.)
else: raise ValueError ( "vintage not in ", vintage_universe )

# PITFALL: These might not look worth defining, but they are!
# That's because we might bifurcate the input and output paths further.
# Currently they bifurcate based only on `vintage`.
# Bifurcation those paths is painful if it requires
# updating every site that uses those paths.
indata  = path.join ( "data",   str(vintage) )
outdata = path.join ( "output", str(vintage) )
