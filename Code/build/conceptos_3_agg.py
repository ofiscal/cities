# aggregate conceptos
#   within muni-year,
#   by broad (usually 2 prefixes, otherwise 3) concepto category

from itertools import chain
import os
import numpy as np
import pandas as pd

import Code.common as c
import Code.util as util
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


concepto_key = pd.read_csv( "output/keys/concepto.csv" )
source       = "output/conceptos_2_subsample/recip-" + str(c.subsample)
dest         = "output/conceptos_3_agg/recip-"       + str(c.subsample)

if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in sm.series:
  df = (
      pd.read_csv( source + "/" + s + ".csv" )
    . drop( columns = [ "Código Concepto" ] ) # soon to be aggregated away
    . rename( columns =
              { "Cód. DANE Municipio" : "muni"
              , "Cód. DANE Departamento" : "dept" } )
    . groupby( by = [
      "year", "muni"
      , "dept" # Given that we already aggregate on muni code,
        # aggregating on dept is redundant,
        # but it's an easy way to retain a non-numeric column after agg(sum).
      , "codigo", "codigo-top" ] )
    . agg( sum )
    . reset_index() )
  if True: # Verify that dept code is redundant given muni code.
    df["one"] = 1
    dtest = ( df .
              groupby( by = ["year","muni","codigo","codigo-top"] ) .
              agg( sum ) )
    assert dtest["one"].max() == 1
    df = df.drop( columns = ["one"] )
    del(dtest)
  df["codigo"] = df["codigo"] . astype(str)
  df = util.to_front(
      ["muni","year","codigo","codigo-top","dept","Concepto"]
    , ( df.merge( concepto_key
                , left_on = "codigo"
                , right_on = "Código Concepto" )
      . drop( columns = [ "Código Concepto" ] ) # redundant given subcode
      . sort_values( ["muni","year","codigo","codigo-top"] ) ) )
  dfs[s] = df
  df.to_csv( dest + "/" + s + ".csv" ,
             index = False )