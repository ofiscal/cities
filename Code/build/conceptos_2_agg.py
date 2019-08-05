# aggregate conceptos
#   within muni-year,
#   by broad (usually 2 prefixes, otherwise 3) concepto category

from itertools import chain
import numpy as np
import pandas as pd
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


concepto_key = pd.read_csv( "output/keys/concepto.csv" )

dfas = {}
for s in sm.series:
  df = (
      pd.read_csv(
        "output/conceptos_1/" + s + ".csv" )
    . drop( columns = [ "Código Concepto" ] ) ) # soon to be aggregated away
  dfa = ( df
          . groupby( by =
            [ "year"
            , "Cód. DANE Municipio"
            , "Cód. DANE Departamento"
               # given muni code, dept is a redundant group, but maybe handy
            , "subcode"
            , "code=subcode" ] )
          . agg( sum )
          . reset_index() )
  dfa["subcode"] = ( dfa["subcode"]
                   . astype( str ) )
  dfa = ( dfa.merge( concepto_key
                   , left_on = "subcode"
                   , right_on = "Código Concepto" )
        . drop( columns = ["Código Concepto"] ) ) # redundant given subcode
  dfas[s] = dfa
  dfa.to_csv( "output/conceptos_2_agg/" + s + ".csv"
            , index = False
  )
