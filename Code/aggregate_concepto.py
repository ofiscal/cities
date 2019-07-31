# Herein a "subcode" is defined as a substring of maximal
# length with no periods in it. For instance, in "ab.cd",
# "ab" is a subcode, but not "a".

from typing import List
import numpy as np
import pandas as pd
from itertools import chain
import re


######
###### exactly_n_subcodes():
###### recognize subcodes, by dividing at periods
######

period_regex : re.Pattern = (
  re.compile( "\." ) )

def exactly_n_subcodes( n : int, s : str ) -> str:
  found = re.findall( period_regex, s )
  l = len( found )
  if l == n-1: return s
  else: return np.nan

assert pd.isnull( exactly_n_subcodes( 2, "b" ) )
assert "a.b" ==   exactly_n_subcodes( 2, "a.b" )
assert pd.isnull( exactly_n_subcodes( 2, "a.b.c" ) )


######
###### first_n_proper_subcodes():
###### find the first few subcodes of a longer code
######

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
  IF it has *more* than n of them. Otherwise return NaN."""
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


######
###### ingresos are special:
###### rather than detecting a fixed number of subcodes,
###### we detect a fixed *set* of them,
###### as defined by ingreso_regex
######

ingreso_regex : re.Pattern = (
  re.compile( "^(TI\.A\.1|TI\.A\.2|TI\.B)" ) )
re.findall( ingreso_regex, "TI.B" )
