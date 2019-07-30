from typing import List
import numpy as np
import pandas as pd
from itertools import chain
import re


no_period_regex : re.Pattern = (
  re.compile( "[^\.]" ) )

def n_code_regex( n : int ) -> re.Pattern:
  preRegex = "[^\.]+\.?"
  return re.compile(
    "".join( ["^"] +
             [ preRegex for _ in range(0,n) ] ) )

def first_n_subcodes( n : int, code : str ) -> List[int]:
  matches = re.findall( n_code_regex(n)
                      , code )
  if not matches:
    return np.nan
  else:
    match = matches[0]
    subcodes = re.findall( no_period_regex
                         , match )
    return subcodes

assert( first_n_subcodes( 2, "a.b.c" ) == ["a","b"] )
assert( first_n_subcodes( 2, "a.b" ) == ["a","b"] )
assert( pd.isnull( first_n_subcodes( 2, "a" ) ) )
