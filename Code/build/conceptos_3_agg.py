# aggregate conceptos
#   within muni-year,
#   by broad (usually 2 prefixes, otherwise 3) concepto category

import os
import numpy as np
import pandas as pd

import Code.common as c
import Code.util as util
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm
import Code.build.conceptos_3_agg_defs as defs


concepto_key = pd.read_csv( "output/keys/concepto.csv" )
source       = "output/conceptos_2_subsample/recip-" + str(c.subsample)
dest         = "output/conceptos_3_agg/recip-"       + str(c.subsample)

if not os.path.exists( dest ):
  os.makedirs(         dest )

group_fields = [
  "year",
  "muni code",
  "dept code",
  "item categ",
  "item top" ]

dfs = {}
for s in sm.series:
  df = (
      pd.read_csv( source + "/" + s + ".csv" )
    . drop( columns = [ "item code" ] ) # soon to be aggregated away
    . groupby( by = group_fields )
    . agg( sum )
    . reset_index() )
  assert defs.group_is_redundant(
    "dept code", group_fields, df )
    # Given that we already aggregate on muni code,
    # aggregating on dept code is redundant,
    # but offers an easy way to keep the column without summing it.
  df["item categ"] = df["item categ"] . astype(str)
  df = util.to_front(
      ["muni code","year","item categ","item top","dept code","item"]
    , ( df.merge( concepto_key
                , left_on = "item categ"
                , right_on = "Código Concepto" )
      . drop( columns = [ "Código Concepto" ] ) # redundant given subcode
      . rename( columns = { "Concepto" : "item" } )
      . sort_values( ["muni code","year","item categ","item top"] ) ) )
  dfs[s] = df
  df.to_csv( dest + "/" + s + ".csv" ,
             index = False )
