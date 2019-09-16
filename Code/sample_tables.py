if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.util as util
  import Code.sample_tables_defs as defs
  import Code.metadata.two_series as ser

if True:
  group_vars = ["dept", "muni", "year"]
  geo_vars   = ["dept", "muni", "dept code", "muni code"]
  assert c.subsample == 1 # This program expects the full sample.

if True: # read data
  raw = {}
  for s in ser.series:
    raw[s.name] = (
      pd.read_csv(
        ( "output/budget_7_verbose/recip-" + str(c.subsample)
          + "/" + s.name + ".csv"),
        encoding = "utf-8" ) .
      sort_values( group_vars ) )

if True: # restrict to the spacetime we need
  spacetime_sample = {}
  for s in ser.series:
    df = raw[s.name]
    df = pd.concat(
      [ #df[ df["muni"].isin( { "BOGOTÁ, D.C.",
        #                       "SANTA MARTA",
        #                       "FILANDIA",
        #                       "VALLE DEL GUAMUEZ" } ) ],
        df[ df["muni code"] .
            isin( { 11001,       # Bogotá D.C., Bogotá D.C.
                    68001,       # Bucaramanga, Santander
                    20710,       # San Alberto, Cesar
                    81001,       # Arauca     , Arauca
                    41298 } ) ], # Garzón     , Huila
        df[ ( df["muni code"] == -1 ) &
            ( df["dept"].isin( [ "ANTIOQUIA",
                                 "CESAR",
                                 "CHOCÓ",
                                 "ARAUCA" ] ) ) ] ],
      axis = "rows" )
    df = ( df[ df["year"] == 2018 ] .
           drop( columns = "year" ) )
    spacetime_sample[s.name] = df

if True: # group all but the biggest five categories
  items_grouped = {}
  for s in ser.series:
    df = spacetime_sample[s.name]
    df = util.to_front(
      ["muni" ,"dept", "item categ", s.pesos_col],
      defs.sum_all_but_greatest_n_rows_in_groups(
        n = 5,
        group_vars = geo_vars,
        sort_vars = [s.pesos_col],
        meaningless_to_sum = ["item categ"],
        df0 = df ) )
    df["item categ"].fillna("other")
    items_grouped[s.name] = df

if True: # output two big tables
  dest = "output/sample_tables/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )
  for s in ser.series:
    items_grouped[s.name].to_csv(
      dest + "/" + s.name + ".csv",
      encoding = "utf-8",
      index = False )

for s in ser.series: # for comparison to integ_tests/iBudget_7_verbose
  print(s.name)
  df = items_grouped[s.name]
  ( df[ ( df["muni"] == "SANTA MARTA" ) |
        ( df["dept"] == "ANTIOQUIA"   )   ]
    [["dept","muni",s.pesos_col,"item categ"]] .
    sort_values( ["dept","muni",s.pesos_col],
                 ascending = False ) )
