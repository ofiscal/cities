# Herein a "subcode" is defined as a substring of maximal
# length with no periods in it. For instance, in "ab.cd",
# "ab" is a subcode, but not "a".

from typing import List
import numpy as np
import pandas as pd
from itertools import chain
import re


no_period_regex : re.Pattern = (
  re.compile( "[^\.]" ) )

def regex_for_more_than_n_codes( n : int ) -> re.Pattern:
  """ If a code had exactly n subcodes,
  the last would have no trailing period. """
  preRegex = "[^\.]+\."
  return re.compile(
    "".join( ["^"] +
             [ preRegex for _ in range(0,n) ] ) )

def first_n_proper_subcodes( n : int, code : str ) -> List[int]:
  """ Finds the first n subcodes of a code,
  but only if it has *more* than n of them. """
  matches = re.findall( regex_for_more_than_n_codes(n)
                      , code )
  if not matches:
    return np.nan
  else:
    match = matches[0]
    subcodes = re.findall( no_period_regex
                         , match )
    return subcodes

assert ["a","b"] == first_n_proper_subcodes( 2, "a.b.c.d" )
assert ["a","b"] == first_n_proper_subcodes( 2, "a.b.c"   )
assert pd.isnull(   first_n_proper_subcodes( 2, "a.b" ) )
assert pd.isnull(   first_n_proper_subcodes( 2, "a"   ) )
