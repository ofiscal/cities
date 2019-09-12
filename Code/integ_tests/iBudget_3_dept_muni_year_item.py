if True:
  import pandas as pd
  import numpy as np
  #
  import Code.build.classify_budget_codes as codes
  import Code.build.use_keys as uk
  import Code.integ_tests.integ_util as iu
  import Code.series_metadata as ser

s3_dfs = {} # stage 3 (build/budget_3_dept_muni_year_item) data frames
for s in ser.series:
  s3_dfs[s.name] = uk.merge_geo(
    pd.read_csv(
      "output/budget_3_dept_muni_year_item/recip-1/" + s.name + ".csv",
      encoding = "utf-16" ) )

if True: # build tax subset
  df = s3_dfs["ingresos"]
  s3_ing = (
    df.copy()
    [   ( df["year"] == iu.year )
      & (   (                df["muni"] == iu.muni )
          | (   ( pd.isnull( df["muni"] ) )
              & (            df["dept"] == iu.dept ) ) ) ] )
  s3_ing["muni"] = s3_ing["muni"].fillna(-1)
  print( "\nThis kind of breakdown adds no extra info for ingresos, but it will for gastos." )
  ( s3_ing
    [["dept","muni","item categ","item recaudo"]] .
    sort_values( ["dept","muni","item categ"] ) )
  print( "\nDATA: budget_3_dept_muni_year_item:" )
  ( s3_ing
    [["dept","muni","item categ","item recaudo"]] .
    groupby( [ "dept","muni","item categ" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item categ"] ) )

