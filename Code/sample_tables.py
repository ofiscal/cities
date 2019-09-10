if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.util as util
  import Code.sample_tables_defs as defs
  import Code.series_metadata as ser


group_vars = ["dept", "muni", "year"]

assert c.subsample == 1 # This program expects the full sample.

if True: # read data
  raw = {}
  for s in ser.series:
    raw[s.name] = (
      pd.read_csv(
        ( "output/budget_7_verbose/recip-" + str(c.subsample)
          + "/" + s.name + ".csv"),
        encoding = "utf-16" ) .
      sort_values( group_vars ) )

if True: # restrict to the munis and depts we need,
         # and sort within group by budget item value
  geo_sample = {}
  for s in ser.series:
    df = raw[s.name]
    geo_sample[s.name] = (
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
      sort_values( group_vars + [s.pesos_col] ) )

if True: # group all but the biggest five categories
  items_grouped = {}
  for s in ser.series:
    df = geo_sample[s.name]
    items_grouped[s.name] = util.to_front(
      group_vars + ["item categ", s.pesos_col],
      defs.sum_all_but_greatest_n_rows_in_groups(
        n = 5,
        group_vars = group_vars,
        sort_vars = [s.pesos_col],
        meaningless_to_sum = ["dept code","muni code","item categ"],
        df0 = df ) )
    if True: # output one big table
      dest = "output/sample_tables/recip-" + str(c.subsample)
      if not os.path.exists( dest ):
        os.makedirs(         dest )
      items_grouped[s.name].to_csv(
        dest + "/" + s.name + ".csv",
        encoding = "utf-16",
        index = False )

def output_pivot( df0 : pd.DataFrame,
                  dest_root : str ):
  df = df0.reset_index() # to restore muni code and dept code
  if True: # get our bearings
    muni_code = str( df["muni code"].iloc[0] )
    dept_code = str( df["dept code"].iloc[0] )
    muni      = str( df["muni"].iloc[0] )
    dept      = str( df["dept"].iloc[0] )
    dest = dest_root + "/" + dept_code + "_" + muni_code
    if not os.path.exists( dest ):
      os.makedirs(         dest )
  if True: # output a readme that says where this is, and a pivot table
    ( df.pivot( index = "item categ",
                columns = "year",
                values = s.pesos_col ) .
      to_csv( dest + "/data.csv", # in this case we *do* want the index
              encoding = "utf-16" ) )
    with open( dest + "/README.txt", "w" ) as f:
      f.write( "Dept: " + dept + "\n" +
               "Muni: " + muni + "\n" )

if True: # write many little pivot tables, one for each place:
         # its columns are years, and its rows item categs
  for s in ser.series:
    df = items_grouped[s.name].copy()
    ( df . groupby( ["dept code","muni code"] ) .
      apply( lambda df:
             output_pivot(
               df0       = df,
               dest_root = "output/sample_pivots" ) ) )

