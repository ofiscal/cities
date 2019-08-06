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
    "".join( ["^("]
           + [ subcode_with_trailing_period
               for _ in range(0,n-1) ]
           + [ subcode_without_trailing_period ]
           + [")"]
    ) )

# a test
df = pd.DataFrame( {"code" : ["1","1.2","1.2.3"]} )
df["subcode"] = df["code"].str.extract( regex_for_at_least_n_codes(2) )
df["code=subcode"] = df["code"] == df["subcode"]
assert df.equals( pd.DataFrame(
  { "code"         : ["1",     "1.2","1.2.3"]
  , "subcode"      : [ np.nan, "1.2", "1.2" ]
  , "code=subcode" : [False,   True,  False ] } ) )


######
###### ingresos are special:
###### rather than detecting a fixed number of subcodes,
###### we detect a fixed *set* of them,
###### namely {"TI.A.1","TI.A.2","TI.B"}
######

ingreso_regex : re.Pattern = (
  re.compile( "^(TI\.A\.1|TI\.A\.2|TI\.B)" ) )

# a test
df = pd.DataFrame( {"code":["TI.A","TI.A.1","TI.A.1.2"] } )
df["subcode"] = df["code"].str.extract( ingreso_regex )
df["code=subcode"] = df["code"] == df["subcode"]
assert df.equals( pd.DataFrame(
  { "code":["TI.A","TI.A.1","TI.A.1.2"]
  , "subcode" : [np.nan, "TI.A.1", "TI.A.1"]
  , "code=subcode" : [False, True, False] } ) )

del(df)
