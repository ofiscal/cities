# This will replace aggregation_regexes.py
import numpy as np
import pandas as pd
import re
from typing import Set

import Code.build.budget_codes_stale.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


def match_budget_codes( d : pd.DataFrame,
                        r : re.Pattern ):
  return d[ ( ~ pd.isnull( d["item code"] .
                           str.extract(r) ) )
            . values ] # "values" turns the "not null" series into an array.
                       # TODO ? I don't know why it's needed.

assert ( # test it
  match_budget_codes(
    pd.DataFrame(       { "item code" : ["TI.A","monkey"] } ),
    re.compile("(TI)") ) .
  equals( pd.DataFrame( { "item code" : ["TI.A"] } ) ) )

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

funcionamiento = re.compile(
  # The only category of interest in funcionamiento is total spending.
  "^(1)$" )

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

