if True:
  import pandas as pd
  import numpy as np
  #
  import Code.build.classify_budget_codes as codes
  import Code.build.use_keys as uk
  import Code.integ_tests.integ_util as iu
  import Code.series_metadata as ser

s5_dfs = {} # stage 5 (build/budget_5_add_regalias) data frames
for s in ser.series:
  df = uk.merge_geo(
    pd.read_csv(
      "output/budget_5_add_regalias/recip-1/" + s.name + ".csv",
      encoding = "utf-16" ) )
  df["muni"] = df["muni"].fillna("dept")
  s5_dfs[s.name] = df

if True: # build tax subset
  df = s5_dfs["ingresos"]
  s5_ing = (
    df.copy()
    [   ( df["year"] == iu.year )
      & (   (     df["muni"] == iu.muni )
          | (   ( df["muni"] == "dept" )
              & ( df["dept"] == iu.dept ) ) ) ] )
  s5_ing["muni"] = s5_ing["muni"].fillna(-1)
  print( "\nThis kind of breakdown adds no extra info for ingresos, but it will for gastos." )
  ( s5_ing
    [["dept","muni","item categ","item recaudo"]] .
    sort_values( ["dept","muni","item categ"] ) )
  print( "\nDATA: budget_5_add_regalias" )
  ( s5_ing
    [["dept","muni","item categ","item recaudo"]] .
    groupby( [ "dept","muni","item categ" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item categ"] ) )

