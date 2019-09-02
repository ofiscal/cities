import os
import pandas as pd

import Code.common as c
import Code.series_metadata as ser


deflator = pd.read_csv( "output/inflation.csv",
                        encoding = "utf-16" )
deflator["deflator"] = ( # normalize in terms of 2018 pesos
  1 / ( deflator["deflator"] /
        float( deflator
               [ deflator["year"] == 2018 ]
               ["deflator"] ) ) )

source = "output/budget_4_scaled/recip-" + str(c.subsample)
dest = "output/budget_5_deflate_and_regalias/recip-" + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs(         dest )

dfs = {}
for s in ser.series:
  name, pesos_col = (s.name, s.pesos_col)
  df = pd.read_csv( source + "/" + name + ".csv",
                    encoding = "utf-16" )
  df = df.merge( deflator, on = "year" )
  df[pesos_col] = df[pesos_col] * df["deflator"]
  df.to_csv( ( dest + "/" + name + ".csv" ),
             index = False,
             encoding = "utf-16" )
