# aggregate conceptos
#   within muni-year,
#   by broad (usually 2 prefixes, otherwise 3) concepto category

from itertools import chain
import numpy as np
import pandas as pd
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


dfas = {}
for s in sm.series:
  df = (
    pd.read_csv(
      "output/conceptos_1/" + s + ".csv" )
    . drop( columns = [
        "Código FUT"            # not useful
      , "Código Concepto" ] ) ) # soon to be aggregated away
  dfa = ( df
          . groupby( by =
            [ "year"
            , "Cód. DANE Municipio"
            , "Cód. DANE Departamento"
               # dept is redundant given muni code, but maybe handy
            , "subcode"
            , "code=subcode" ] )
          . agg( sum ) )
  dfa.to_csv( "output/conceptos_2_agg/" + s + ".csv" )
  dfas[s] = dfa
