if True:
  import numpy                                as np
  import os
  import pandas                               as pd
  #
  import Code.common                          as c
  import Code.metadata.two_series             as ser
  import Code.util.aggregate_all_but_biggest  as defs
  import Code.util.misc                       as util


if True:
  group_vars = ["dept", "muni", "year"]
  geo_vars   = ["dept", "muni", "dept code", "muni code"]
  assert c.subsample == 1 # This program expects the full sample.

if True: # read data
  raw = {}
  for s in ser.series:
    raw[s.name] = (
      pd.read_csv(
        os.path.join ( c.outdata, "budget_7_verbose",
                       "recip-" + str(c.subsample),
                       s.name + ".csv") ) .
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
           drop( columns = "year" ) .
           sort_values( ["dept","muni"] + s.money_cols ) )
    spacetime_sample[s.name] = df

if True: # group all but the biggest five categories
  items_grouped = {}
  for s in ser.series:
    df = spacetime_sample[s.name]
    df = util.to_front(
      ["muni" ,"dept", "item categ"] + s.money_cols,
      defs.sum_all_but_greatest_n_rows_in_groups(
        n = 5,
        group_vars = geo_vars,
        sort_vars = s.money_cols,
        meaningless_to_sum = ["item categ"],
        df0 = df ) )
    df["item categ"].fillna("other")
    items_grouped[s.name] = df

if True: # output two big tables
  dest = os.path.join ( c.outdata, "sample_tables",
                        "recip-" + str(c.subsample) )
  if not os.path.exists( dest ):
    os.makedirs(         dest )
  for s in ser.series:
    for (source,suffix) in [ (spacetime_sample,""),
                             (items_grouped,"_grouped") ]:
      source[s.name].to_excel(
        dest + "/" + s.name + suffix + ".xlsx",
        index = False )
      source[s.name].to_csv(
        dest + "/" + s.name + suffix +".csv",
        index = False )

if False: # for comparison to integ_tests/iBudget_7_verbose
  for s in ser.series:
    print(s.name)
    df = items_grouped[s.name]
    ( df[ ( df["muni"] == "SANTA MARTA" ) |
          ( df["dept"] == "ANTIOQUIA"   )   ]
      [["dept","muni"] + s.money_cols + ["item categ"]] .
      sort_values( ["dept","muni",s.pesos_col],
                   ascending = False ) )
