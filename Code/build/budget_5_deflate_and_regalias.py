import os
import pandas as pd

import Code.common as c
import Code.series_metadata as ser


######
###### Ingest primary data
######

source = "output/budget_4_scaled/recip-" + str(c.subsample)
dest = "output/budget_5_deflate_and_regalias/recip-" + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in ser.series:
  dfs[s.name] = pd.read_csv( source + "/" + s.name + ".csv",
                             encoding = "utf-16" )


######
###### Add regalias
######

regalias = (
  pd.read_csv( "output/regalias.csv",
               encoding="utf-16" ) .
  rename( columns = { "regalias" :
                      ser.series_dict["ingresos"].pesos_col } ) )
regalias["item code"] = "regalías"
regalias["item"] = "regalías"

dfs["ingresos"] = pd.DataFrame.append( dfs["ingresos"], regalias,
                                       sort = False )


######
###### Deflate
######

deflator = pd.read_csv( "output/inflation.csv",
                        encoding = "utf-16" )
deflator["deflator"] = ( # normalize in terms of 2018 pesos
  1 / ( deflator["deflator"] /
        float( deflator
               [ deflator["year"] == 2018 ]
               ["deflator"] ) ) )

for s in ser.series:
  df = dfs[s.name]
  df = df.merge( deflator, on = "year" )
  df[s.pesos_col] = df[s.pesos_col] * df["deflator"]
  dfs[s.name] = df
  df.to_csv( ( dest + "/" + s.name + ".csv" ),
             index = False,
             encoding = "utf-16" )
