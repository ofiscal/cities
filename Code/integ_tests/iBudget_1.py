if True:
  import pandas as pd
  import numpy as np
  #
  import Code.metadata.terms as t
  import Code.metadata.raw_series as sm
  import Code.build.use_keys as uk
  import Code.build.classify_budget_codes as codes


s1_dfs = {} # stage 1 (build/budget_1) data frames
for s in sm.series:
  s1_dfs[s] = uk.merge_geo(
    pd.read_csv(
      "output/budget_1/" + s + ".csv") )

assert len( s1_dfs["ingresos"] )       == (862536 -6)
assert len( s1_dfs["inversion"] )      == (1525207 -6 -90)
  # I checked these 90 missing rows
  # (see Code/explore/find_missing_rows.py)
  # and they involve no codes that we need.
assert len( s1_dfs["funcionamiento"] ) == (1258055 -6)
assert len( s1_dfs["deuda"] )          == (44870 -6)

if True: # build tax subset
  df = s1_dfs["ingresos"]
  s1_ing = (
    df.copy()
    [   ( df["item code"] .
          isin( codes.of_interest["ingresos"] ) )
      & ( df["year"] == 2018 )
      & (   (                df["muni"] == "SANTA MARTA" )
          | (   ( pd.isnull( df["muni"] ) )
              & (            df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s1_ing["muni"] = s1_ing["muni"].fillna(-1)
  print( "\nSTAGE 1:" )
  ( s1_ing
    [["dept","muni","item code","item recaudo"]] .
    sort_values( ["dept","muni","item code"] ) )
  ( s1_ing
    [["dept","muni","item code","item recaudo"]] .
    groupby( [ "dept","muni","item code" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item code"] ) )

for f in [t.inversion,t.funcionamiento,t.deuda]: # build gastos subsets
  df = s1_dfs[f]
  s1_ing = (
    df.copy()
    [   ( df["item code"] .
          isin( codes.of_interest[f] ) )
      & ( df["year"] == 2018 )
      & (   (                df["muni"] == "SANTA MARTA" )
          | (   ( pd.isnull( df["muni"] ) )
              & (            df["dept"] == "ANTIOQUIA" ) ) ) ] )
  s1_ing["muni"] = s1_ing["muni"].fillna(-1)
  print( "\n", f )
  print( "\nSTAGE 1:" )
  ( s1_ing
    [["dept","muni","item code","item oblig"]] .
    sort_values( ["dept","muni","item code"] ) )
  ( s1_ing
    [["dept","muni","item code","item oblig"]] .
    groupby( [ "dept","muni","item code" ] ) .
    agg( sum ) .
    sort_values( ["dept","muni","item code"] ) )

