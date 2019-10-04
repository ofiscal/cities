if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.two_series as ser

if True: # folders
  source = "output/budget_5_add_regalias/recip-" + str(c.subsample)
  dest   = "output/budget_6_deflate/recip-"      + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input data
  dfs = {}
  for s in ser.series:
    dfs[s.name] = pd.read_csv( source + "/" + s.name + ".csv" )
  deflator = pd.read_csv( "output/inflation.csv" )
  deflator["deflator"] = ( # normalize in terms of 2018 pesos
    1 / ( deflator["deflator"] /
          float( deflator
                 [ deflator["year"] == 2018 ]
                 ["deflator"] ) ) )

for s in ser.series:
  df = dfs[s.name]
  df = df.merge( deflator, on = "year" )
  for c in s.money_cols:
    df[c] = df[c] * df["deflator"]
  df = df.drop( columns = ["deflator"] )
  dfs[s.name] = df
  df.to_csv( dest + "/" + s.name + ".csv",
             index = False )

