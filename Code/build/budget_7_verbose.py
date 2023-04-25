# Merge verbal names of depts and munis back into the data.

if True:
  import numpy                      as np
  import os
  import pandas                     as pd
  #
  import Code.build.use_keys        as uk
  import Code.common                as c
  import Code.metadata.four_series  as s4
  import Code.util.misc             as util


if True: # folders
  source = os.path.join ( c.outdata,
                          "budget_6p7_avg_muni",
                          "recip-" + str(c.subsample) )
  dest = os.path.join ( c.outdata, "budget_7_verbose",
                        "recip-" + str(c.subsample) )
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # Merge geo data into main data.
  dfs = {}
  for s in s4.series:
    extra_columns = ( ["munis in dept","muni-years in dept"]
                      if s.name[-4:] == "-pct"
                      else [] )
    sn = s.name
    df = util.to_front(
      ["dept","muni","year"] + s.money_cols + ["item categ"],
      uk.merge_geo(
        pd.read_csv (
          os.path.join ( source,
                         sn + ".csv" ) )
        [ ["muni code","dept code","year","item categ"]
          + extra_columns + s.money_cols] ) )
    df.loc[ df["muni code"] == 0,
            "muni" ] = "dept"
    df.loc[ df["muni code"] == -2,
            "muni" ] = "promedio"
    df.to_csv( dest + "/" + s.name + ".csv",
               index = False )
    dfs[sn] = df
