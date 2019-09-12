if True:
  import pandas as pd
  import numpy as np
  #
  import Code.integ_tests.integ_util as iu
  import Code.series_metadata as ser
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes

s6_dfs = {} # stage 6 (build/budget_6_deflate) data frames
for s in ser.series:
  df = uk.merge_geo(
    pd.read_csv(
      "output/budget_6_deflate/recip-1/" + s.name + ".csv",
      encoding = "utf-16" ) )
  df["muni"] = df["muni"].fillna("dept")
  s6_dfs[s.name] = df

if True: # build tax subset
  df = s6_dfs["ingresos"]
  s6_ing = (
    df.copy()
    [   ( df["year"] == iu.year )
      & (   (     df["muni"] == iu.muni )
          | (   ( df["muni"] == "dept" )
              & ( df["dept"] == iu.dept ) ) ) ] )
  s6_ing["muni"] = s6_ing["muni"].fillna(-1)
  print( "\nThis kind of breakdown adds no extra info for ingresos, but it will for gastos." )
  ( s6_ing
    [["dept","muni","item categ","item recaudo"]] .
    sort_values( ["dept","muni","item categ"] ) )
  print( "\nDATA: budget_6_deflate" )
  ( s6_ing
    [["dept","muni","item categ","item recaudo"]] .
    groupby( [ "dept","muni","item categ" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item categ"] ) )

