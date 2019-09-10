# Merge verbal names of depts and munis back into the data.

if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.util as util
  import Code.series_metadata as ser
  import Code.build.use_keys as uk

if True: # merge geo data into main data
  if True: # folders
    source   = "output/budget_6_deflate/recip-" + str(c.subsample)
    dest = "output/budget_7_verbose/recip-" + str(c.subsample)
    if not os.path.exists( dest ):
      os.makedirs(         dest )
  dfs = {}
  for s in ser.series:
    sn = s.name
    df = util.to_front(
      ["dept","muni","year",s.pesos_col,"item categ"],
      uk.merge_geo(
        pd.read_csv( source + "/" + sn + ".csv",
                     encoding = "utf-16" )
        [["muni code","dept code","year","item categ",
          s.pesos_col]] ) )
    df["muni"] = df["muni"] . fillna("dept")
    df.to_csv( dest + "/" + s.name + ".csv",
               encoding = "utf-16",
               index = False )
    dfs[sn] = df
