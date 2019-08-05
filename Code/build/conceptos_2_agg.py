# aggregate conceptos
#   within muni-year,
#   by broad (usually 2 prefixes, otherwise 3) concepto category

from itertools import chain
import numpy as np
import pandas as pd
import Code.util as util
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


concepto_key = pd.read_csv( "output/keys/concepto.csv" )

dfs = {}
for s in sm.series:
  df = (
      pd.read_csv( "output/conceptos_1/" + s + ".csv" )
    . drop( columns = [ "Código Concepto" ] ) # soon to be aggregated away
    . groupby( by =
      [ "year"
      , "Cód. DANE Municipio"
      , "Cód. DANE Departamento" # given that we aggregate on muni code,
         # aggregating on dept is redundant,
         # but an easy way to retain the variable
      , "subcode"
      , "code=subcode" ] )
    . agg( sum )
    . reset_index() )
  df["subcode"] = ( df["subcode"]
                   . astype( str ) )
  df = util.to_front(
      ["muni","year","subcode","code=subcode","dept","Concepto"]
    , ( df.merge( concepto_key
                , left_on = "subcode"
                , right_on = "Código Concepto" )
      . drop( columns = ["Código Concepto"] ) # redundant given subcode
      . rename( columns =
                { "Cód. DANE Municipio" : "muni"
                , "Cód. DANE Departamento" : "dept" } )
      . sort_values( ["muni","year","subcode","code=subcode"] ) ) )
  dfs[s] = df
  df.to_csv( "output/conceptos_2_agg/" + s + ".csv"
            , index = False
  )
