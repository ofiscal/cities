# Herein a "subcode" is defined as a substring of maximal
# length with no periods in it. For instance, in "ab.cd",
# "ab" is a subcode, but not "a".

from typing import List
import numpy as np
import pandas as pd
from itertools import chain
import re


######
###### Regexes for aggregating codes to the first two subcodes.
######

def regexes_for_2_codes() -> (re.Pattern,re.Pattern,re.Pattern):
  """ See tests, immediately below function definition. """
  category = re.compile( "^([^\.]+\.[^\.]+)" )
  top      = re.compile( "^([^\.]+\.[^\.]+)$" )
  child    = re.compile( "^([^\.]+\.[^\.]+\.[^\.]+)$" )
  return (category, top, child)

if True: # test regexes_for_2_codes
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


######
###### Ingresos are special:
###### Rather than detecting a fixed number of subcodes,
###### we detect an explicit set of them,
###### namely {"TI.A.1","TI.A.2","TI.B"}.
######
# (This strategy would also work for the other series,
# but fortunately, in those (non-ingreso) cases
# we don't need to enumerate every possible prefix,
# because we always want the first two.)

def regexes_for_ingresos() -> (re.Pattern,re.Pattern,re.Pattern):
  """ See tests, immediately below function definition. """
  three_kinds = "TI\.A\.1|TI\.A\.2|TI\.B"
  category = re.compile( "^(" + three_kinds + ")" )
  top      = re.compile( "^(" + three_kinds + ")$" )
  child    = re.compile( "^(" + three_kinds + "\.[^\.]+)$" )
  return (category, top, child)

if True: # test regexes_for_ingresos
  df = pd.DataFrame( {"code" : [
      "TI"
    , "TI.B"
    , "TI.B.22"
    , "TI.B.22.33"
    , "1.2" # does not start with TI, hence should not work
  ]} )
  cat,top,child = regexes_for_ingresos()
  df["cat"]   =              df["code"].str.extract( cat )
  df["top"]   = ~ pd.isnull( df["code"].str.extract( top ) )
  df["child"] = ~ pd.isnull( df["code"].str.extract( child ) )
  assert df.equals( pd.DataFrame(
    { "code"  : ["TI",   "TI.B", "TI.B.22", "TI.B.22.33", "1.2"]
    , "cat"   : [np.nan, "TI.B", "TI.B"   , "TI.B",       np.nan ]
    , "top"   : [False,   True,  False,     False,        False]
    , "child" : [False,   False, True,      False,        False]
    } ) )
