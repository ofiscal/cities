# PURPOSE:
#   (1) Cull: This is obsolete
#     This program used to drop some unneeded columns, rows.
#     Now that happens upstream.
# Switch from two series to four:
#   Initial 2: gastos, ingresos
#   Final 4: gastos, gastos-pct, ingresos, ingresos-pct
#     In the -pct files, convert peso values to percentages.

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  #
  import Code.common as c
  from Code.util.percentify import percentify_columns
  import Code.metadata.two_series as s2
  import Code.metadata.four_series as s4

if True: # folders
  source = "output/budget_6_deflate/recip-"               + str(c.subsample)
  dest   = "output/budget_6p5_cull_and_percentify/recip-" + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

spacetime = ["dept code","muni code","year"]

if True: # input data
  dfs = {}
  for s in s2.series:
    df = pd.read_csv(
      source + "/" + s.name + ".csv" )
    df = ( # drop some columns, rows. OBSOLETE --
           # those are now already dropped upstream.
      df[df["year"] >= 2013]
        # because there is no regalias data before 2013
           [spacetime + ["item categ"] + s.money_cols] )
        # this line drops the money columns we don't use
    dfs[s.name] = df

for s in s2.series:
  df = dfs[s.name].copy()
  df = ( df . groupby(spacetime) .
         apply( lambda df:
                percentify_columns(
                  s.money_cols, df ) ) .
         reset_index( drop=True) )
  dfs[s.name + "-pct"] = df

for s in s2.series:
  m = ( dfs[s.name] .
        sort_values(spacetime) .
        reset_index(drop=True) )
  p = ( dfs[s.name + "-pct"] .
        sort_values(spacetime) .
        reset_index(drop=True) )
  assert m.columns.equals( p.columns )
  assert ( m[spacetime].reset_index() .
           equals(p[spacetime].reset_index() ) )

for s in s4.series:
  dfs[s.name].to_csv( dest + "/" + s.name + ".csv",
                      index = False )
