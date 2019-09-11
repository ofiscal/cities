if True:
  import pandas as pd
  import numpy as np
  #
  import Code.series_metadata as ser
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes

s7_dfs = {} # stage 7 (build/budget_7_verbose) data frames
for s in ser.series:
  s7_dfs[s.name] = pd.read_csv(
    "output/budget_7_verbose/recip-1/" + s.name + ".csv",
    encoding = "utf-16" )

for s in ser.series:
  print( s7_dfs[s.name].columns )

if True: # build tax subset
  df = s7_dfs["ingresos"]
  s7_ing = (
    df.copy()
    [   ( df["year"] == 2018 )
      & (   (     df["muni"] == "SANTA MARTA" )
          | (   ( df["muni"] == "dept" )
              & ( df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s7_ing["muni"] = s7_ing["muni"].fillna(-1)
  print( "\nDATA: budget_7_verbose" )
  ( s7_ing
    [["dept","muni","item categ","item recaudo"]] .
    sort_values( ["dept","muni","item categ"] ) )
  ( s7_ing
    [["dept","muni","item categ","item recaudo"]] .
    groupby( [ "dept","muni","item categ" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item categ"] ) )

