if True:
  import pandas as pd
  import numpy as np
  #
  import Code.series_metadata as ser
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes

s5_dfs = {} # stage 5 (build/budget_5_add_regalias) data frames
for s in ser.series:
  s5_dfs[s.name] = uk.merge_geo(
    pd.read_csv(
      "output/budget_5_add_regalias/recip-1/" + s.name + ".csv",
      encoding = "utf-16" ) )

for s in ser.series:
  print( s5_dfs[s.name].columns )

if True: # build tax subset
  df = s5_dfs["ingresos"]
  s5_ing = (
    df.copy()
    [   ( df["year"] == 2018 )
      & (   (     df["muni"] == "SANTA MARTA" )
          | (   ( df["muni"] == "dept" )
              & ( df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s5_ing["muni"] = s5_ing["muni"].fillna(-1)
  print( "\nDATA: budget_5_add_regalias" )
  ( s5_ing
    [["dept","muni","item categ","item recaudo"]] .
    sort_values( ["dept","muni","item categ"] ) )
  ( s5_ing
    [["dept","muni","item categ","item recaudo"]] .
    groupby( [ "dept","muni","item categ" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item categ"] ) )

