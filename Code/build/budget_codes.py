# This will replace aggregation_regexes.py
import numpy as np
import pandas as pd
import re


ingresos = re.compile(
  # To recognize our "top" ingresos categories of interest:
  # TI.A, TI.B, and TI.A.2.6 """
  "^(TI\." +
  "(?:A|B|A\.2\.6)" +
    # The leading ?: creates a non-capturing group.
    # This groups the alternatives, so that the | operators bind
    # before the rest of the string in the "child" case.
  ")$" ) # The $ guarantees no more subcodes follow,
       # i.e. that we're looking at a top category (e.g. hospitals)
       # and not one of its descendents (e.g. gloves for a hospital).
if True: # test
  s = pd.Series( [ "TI",
                   "TI.A",
                   "TI.A.2",
                   "TI.A.2.6",
                   "11.22" ] )
  t = pd.Series( [ np.nan, "TI.A", np.nan, "TI.A.2.6", np.nan ] )
  assert ( s . str.extract( ingresos ) .
           iloc[:,0] . # str.extract produces a data frame,
                       # so take the first column
           equals( t ) )

two_subcodes = re.compile(
  # To recognize any budget item with exactly two subcodes,
  # e.g. "TI.A" or "A.2" but not "A" or "A.2.1".
  "^(" +
  "[^\.]+\.[^\.]+" +
  ")$" )
if True: # test
  s = pd.Series( [ "11",
                   "11.",
                   "11.22",
                   "11.22.",
                   "11.22.33" ] )
  t = pd.Series( [ np.nan, np.nan, "11.22", np.nan, np.nan ] )
  assert ( s .
           str.extract( two_subcodes ) .
           iloc[:,0] . # str.extract produces a data frame,
                       # so take the first column
           equals( t ) )

