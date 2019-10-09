if True:
  import pandas as pd
  import numpy as np
  #
  import Code.metadata.terms as t
  import Code.metadata.raw_series as raw
  import Code.integ_tests.integ_util as iutil
  import Code.build.classify_budget_codes as codes
  import Code.build.use_keys as uk

if True:
  s0_dfs = {} # stage 0 frames
  for s in raw.series:
    s0_dfs[s] = uk.merge_geo(
      pd.read_csv(
        "output/budget_0_collect/" + s + ".csv") )

def money_col( str ):
  if str == "ingresos":
    return "item total"
  else:
    return "item oblig"

for f in [t.ingresos, t.inversion,t.funcionamiento,t.deuda]:
  print( "\n", f )
  df = s0_dfs[f]
  s0_ing = (
    df.copy()
    [   ( df["item code"] .
          isin( codes.of_interest[f] ) )
      & ( df["year"] == 2018 )
      & (   (                df["muni"] == "SANTA MARTA" )
          | (   ( pd.isnull( df["muni"] ) )
              & (            df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s0_ing["muni"] = (
    s0_ing["muni"] .
    fillna("dept") )
  print( "\nSTAGE 0:" )
  ( s0_ing
    [["dept","muni","item code",money_col(f)]] .
    sort_values( ["dept","muni","item code"] ) )
  ( s0_ing
    [["dept","muni","item code",money_col(f)]] .
    groupby( [ "dept","muni","item code" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item code"] ) )

