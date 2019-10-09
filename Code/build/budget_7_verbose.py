# Merge verbal names of depts and munis back into the data.

if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.util.misc as util
  import Code.metadata.four_series as s4
  import Code.build.use_keys as uk

if True: # folders
  source = "output/budget_6p7_avg_muni/recip-" + str(c.subsample)
  dest = "output/budget_7_verbose/recip-"      + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # merge geo data into main data
  dfs = {}
  for s in s4.series:
    sn = s.name
    df = util.to_front(
      ["dept","muni","year"] + s.money_cols + ["item categ"],
      uk.merge_geo(
        pd.read_csv( source + "/" + sn + ".csv" )
        [ ["muni code","dept code","year","item categ"]
          + s.money_cols] ) )
    df.loc[ df["muni code"] == 0,
            "muni" ] = "dept"
    df.loc[ df["muni code"] == -2,
            "muni" ] = "promedio"
    df.to_csv( dest + "/" + s.name + ".csv",
               index = False )
    dfs[sn] = df

