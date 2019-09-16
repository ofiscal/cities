import os
import pandas as pd

import Code.common as c
import Code.metadata.two_series as ser


source = "output/budget_5_add_regalias/recip-" + str(c.subsample)
dest   = "output/budget_6_deflate/recip-"      + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in ser.series:
  dfs[s.name] = pd.read_csv( source + "/" + s.name + ".csv",
                             encoding = "utf-8" )

deflator = pd.read_csv( "output/inflation.csv",
                        encoding = "utf-8" )
deflator["deflator"] = ( # normalize in terms of 2018 pesos
  1 / ( deflator["deflator"] /
        float( deflator
               [ deflator["year"] == 2018 ]
               ["deflator"] ) ) )

for s in ser.series:
  df = dfs[s.name]
  df = df.merge( deflator, on = "year" )
  df[s.pesos_col] = df[s.pesos_col] * df["deflator"]
  df = df.drop( columns = ["deflator"] )
  dfs[s.name] = df
  df.to_csv( dest + "/" + s.name + ".csv",
             index = False,
             encoding = "utf-8" )
