# This adds regalias to the ingresos data.
# It just copies the gastos data unchanged to a new directory --
# CPU-inefficient, yes, but safer than doing something more confusing.

import os
import pandas as pd

import Code.common as c
import Code.series_metadata as ser


source = "output/budget_4_scaled/recip-"       + str(c.subsample)
dest   = "output/budget_5_add_regalias/recip-" + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in ser.series:
  dfs[s.name] = pd.read_csv( source + "/" + s.name + ".csv",
                             encoding = "utf-16" )

regalias = (
  pd.read_csv( "output/regalias.csv",
               encoding="utf-16" ) .
  rename( columns = { "regalias" :
                      ser.series_dict["ingresos"].pesos_col } ) )
regalias["item code"] = "regalías"
regalias["item"] = "regalías"

dfs["ingresos"] = pd.DataFrame.append( dfs["ingresos"],
                                       regalias,
                                       sort = False )

for s in ser.series:
  dfs[s.name].to_csv( dest + "/" + s.name + ".csv",
                      index = False,
                      encoding = "utf-16" )
