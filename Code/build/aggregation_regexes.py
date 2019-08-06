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

def regexes_for_2_codes() -> (re.Pattern,re.Pattern,re.Pattern):
  """ See tests, immediately below function definition. """
  category = re.compile( "^([^\.]+\.[^\.]+)" )
  top      = re.compile( "^([^\.]+\.[^\.]+)$" )
  child    = re.compile( "^([^\.]+\.[^\.]+\.[^\.]+)$" )
  return (category, top, child)

df = pd.DataFrame( {"code" : [ "11"
                             , "11.22"
                             , "11.22.33"
                             , "11.22.33.44" ]} )
cat,top,child = regexes_for_2_codes()
df["cat"]   =              df["code"].str.extract( cat )
df["top"]   = ~ pd.isnull( df["code"].str.extract( top ) )
df["child"] = ~ pd.isnull( df["code"].str.extract( child ) )
assert df.equals( pd.DataFrame(
  { "code"  : ["11"   , "11.22", "11.22.33", "11.22.33.44"]
  , "cat"   : [ np.nan, "11.22", "11.22"   , "11.22" ]
  , "top"   : [False,   True,    False,      False]
  , "child" : [False,   False,   True,       False]
  } ) )


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
