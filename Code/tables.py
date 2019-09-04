if True:
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.tables_defs as defs
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
  munis = geo[["muni code","muni"]]

if True: # merge geo data into main data
  source   = "output/budget_6_deflate/recip-1"
  dfs = {}
  for s in ser.series:
    sn = s.name
    df = ( pd.read_csv( source + "/" + sn + ".csv",
                        encoding = "utf-16" )
           [["muni code","dept code","year","item","item code",
             s.pesos_col]] )
    df = df.merge( munis,
                   how = "left", # b/c in geo, muni code is never -1
                   on = ["muni code"] )
    df = df.merge( depts,
                   on = ["dept code"] )
    dfs[sn] = df

if True: # restrict to the munis and depts we need,
         # and sort by budget item value
  sample = {}
  for s in ser.series:
    df = dfs[s.name]
    sample[s.name] = (
      pd.concat(
        [ df[ df["muni"].isin( { "BOGOTÁ, D.C.",
                                 "SANTA MARTA",
                                 "FILANDIA",
                                 "VALLE DEL GUAMUEZ" } ) ],
          df[ ( df["muni code"] == -1 ) &
              ( df["dept"].isin( [ "ANTIOQUIA",
                                   "CESAR",
                                   "CHOCÓ",
                                   "ARAUCA" ] ) ) ] ],
        axis = "rows" ) .
      sort_values( [ "dept code", "muni code", "year",
                     s.pesos_col ] ) )

if True:
  items_grouped = {}
  group_vars = ["dept", "muni", "year"]
  for s in ser.series:
    df = sample[s.name]
    items_grouped[s.name] = (
      pd.concat(
        [ defs.first_n_in_groups( 5,
                                  group_vars,
                                  df ),
          defs.sum_all_but_first_n_rows_in_groups( 5,
                                                   group_vars,
                                                   df ) ],
        sort = True ) .
      sort_values( ["dept","muni","year",s.pesos_col] ) )

items_grouped["gastos"][["muni","year","item code","item oblig"]]
