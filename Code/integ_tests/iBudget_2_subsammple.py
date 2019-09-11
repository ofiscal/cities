if True:
  import pandas as pd
  import numpy as np
  #
  import Code.series_metadata as ser
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes

s2_dfs = {} # stage 2 (build/budget_2_subsample) data frames
for s in ser.series:
  s2_dfs[s.name] = uk.merge_geo(
    pd.read_csv(
      "output/budget_2_subsample/recip-1/" + s.name + ".csv",
      encoding = "utf-16" ) )

for s in ser.series:
  print( s2_dfs[s.name].columns )

if True: # build tax subset
  df = s2_dfs["ingresos"]
  s2_ing = (
    df.copy()
    [   ( df["item code"] .
          isin( codes.of_interest["ingresos"] ) )
      & ( df["year"] == 2018 )
      & (   (                df["muni"] == "SANTA MARTA" )
          | (   ( pd.isnull( df["muni"] ) )
              & (            df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s2_ing["muni"] = s2_ing["muni"].fillna(-1)
  print( "\nDATA: budget_2_subsample:" )
  ( s2_ing
    [["dept","muni","item code","item recaudo"]] .
    sort_values( ["dept","muni","item code"] ) )
  ( s2_ing
    [["dept","muni","item code","item recaudo"]] .
    groupby( [ "dept","muni","item code" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item code"] ) )

