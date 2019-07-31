# Herein a "subcode" is defined as a substring of maximal
# length with no periods in it. For instance, in "ab.cd",
# "ab" is a subcode, but not "a".

from typing import List
import numpy as np
import pandas as pd
from itertools import chain
import re


######
###### find a fixed number of leading subcodes
######

def regex_for_at_least_n_codes( n : int ) -> re.Pattern:
  """ If a code has exactly n subcodes,
  the last includes no trailing period. """
  subcode_with_trailing_period    = "[^\.]+\."
  subcode_without_trailing_period = "[^\.]+"
  return re.compile(
    "".join( ["^"]
           + [ subcode_with_trailing_period for _ in range(0,n-1) ]
           + [ subcode_without_trailing_period ] ) )

def first_n_subcodes( n : int, code : str ) -> (str,bool):
  """ Finds the first n subcodes of a code,
  if they exist. Otherwise returns NaN."""
  matches = re.findall( regex_for_at_least_n_codes(n)
                      , code )
  if not matches: return ( "", False )
    # The bool is in this case irrelevant
  else: return ( matches[0]
               , matches[0] == code )

assert first_n_subcodes( 2, "1" )     == (""   , False)
assert first_n_subcodes( 2, "1.2" )   == ("1.2", True)
assert first_n_subcodes( 2, "1.2.3" ) == ("1.2", False)


######
###### ingresos are special:
###### rather than detecting a fixed number of subcodes,
###### we detect a fixed *set* of them,
###### namely {"TI.A.1","TI.A.2","TI.B"}
######

ingreso_regex : re.Pattern = (
  re.compile( "^(TI\.A\.1|TI\.A\.2|TI\.B)" ) )
re.findall( ingreso_regex, "TI.B" )

def ingreso_subcodes( code : str ) -> (str,bool):
  matches = re.findall( ingreso_regex
                      , code )
  if not matches: return ( "", False )
    # The bool is in this case irrelevant
  else: return ( matches[0]
               , matches[0] == code )

assert ingreso_subcodes( "TI.A.1"   ) == ("TI.A.1", True )
assert ingreso_subcodes( "TI.A.1.2" ) == ("TI.A.1", False)
assert ingreso_subcodes( "TI.A" )     == (""      , False)
