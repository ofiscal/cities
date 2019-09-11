if True:
  import pandas as pd
  import numpy as np
  #
  import Code.series_metadata as ser
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes

s4_dfs = {} # stage 4 (build/budget_4_scaled) data frames
for s in ser.series:
  s4_dfs[s.name] = uk.merge_geo(
    pd.read_csv(
      "output/budget_4_scaled/recip-1/" + s.name + ".csv",
      encoding = "utf-16" ) )

for s in ser.series:
  print( s4_dfs[s.name].columns )

if True: # build tax subset
  df = s4_dfs["ingresos"]
  s4_ing = (
    df.copy()
    [   ( df["year"] == 2018 )
      & (   (                df["muni"] == "SANTA MARTA" )
          | (   ( pd.isnull( df["muni"] ) )
              & (            df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s4_ing["muni"] = s4_ing["muni"].fillna(-1)
  print( "\nThis kind of breakdown adds no extra info for ingresos, but it will for gastos." )
  ( s4_ing
    [["dept","muni","item categ","item recaudo"]] .
    sort_values( ["dept","muni","item categ"] ) )
  print( "\nDATA: budget_4_scaled:" )
  ( s4_ing
    [["dept","muni","item categ","item recaudo"]] .
    groupby( [ "dept","muni","item categ" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item categ"] ) )

