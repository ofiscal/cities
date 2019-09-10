# Merge verbal names of depts and munis back into the data.

if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.util as util
  import Code.series_metadata as ser

if True: # geo data
  geo = (
    pd.read_csv( "output/keys/geo.csv",
                 encoding = "utf-16" ) .
    rename( columns =
            { "Cód. DANE Municipio"      : "muni code",
              "Cód. DANE Departamento"   : "dept code",
              "Nombre DANE Municipio"    : "muni",
              "Nombre DANE Departamento" : "dept" } ) )
  depts = ( geo[["dept code","dept"]] .
            groupby( "dept code" ) .
            agg('first') .
            reset_index() )
  assert depts.shape == (33,2)
  assert pd.isnull(depts).any().any() == False
  munis = geo[["muni code","muni"]]
  assert munis.shape == (1101,2)
  assert pd.isnull(munis).any().any() == False

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
      ( ( pd.read_csv( source + "/" + sn + ".csv",
                       encoding = "utf-16" )
          [["muni code","dept code","year","item categ",
            s.pesos_col]] ) .
        merge( munis,
               how = "left", # b/c in geo, muni code is never -1
               on = ["muni code"] ) .
        merge( depts,
               on = ["dept code"] ) ) )
    df.to_csv( dest + "/" + s.name + ".csv",
               encoding = "utf-16",
               index = False )
    dfs[sn] = df
