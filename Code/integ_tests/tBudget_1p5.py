if True:
  import pandas as pd
  import numpy as np
  #
  import Code.build.classify_budget_codes as codes
  import Code.build.use_keys as uk
  import Code.integ_tests.integ_util as iu
  import Code.metadata.two_series as s2

name_of_data_source = "budget_1p5"

s1p5_dfs = {} # stage 1.5 (build/budget_1p5) data frames
for name in ["ingresos","gastos"]:
  s1p5_dfs[name] = uk.merge_geo(
      pd.read_csv( "output/" + name_of_data_source +
                   "/" + name + ".csv" ) )

for s in ["ingresos","gastos"]:
  print( len(s1p5_dfs[s]) )

if True:
  smaller = {} # a spacetime subset of that input data
  for (name,cs) in [
      ("ingresos",codes.of_interest["ingresos"]),
      ("gastos",set.union(
        codes.of_interest["inversion"],
        codes.of_interest["funcionamiento"],
        codes.of_interest["deuda"] ) ) ]:
    df = s1p5_dfs[name]
    smaller[name] = (
      df.copy()
      [   ( df["item code"] .
            isin(cs) )
        & ( df["year"] == iu.year )
        & (   (                df["muni"] == iu.muni )
            | (   ( pd.isnull( df["muni"] ) )
                & (            df["dept"] == iu.dept ) ) ) ] )
    smaller[name]["muni"] = (
      smaller[name]["muni"].fillna("dept") )
  if True:
    for (name,money_column) in [
        ("ingresos","item total"),
        ("gastos","item oblig") ]:
      print(
        "\DISAGGREGATED: " + name_of_data_source + ": " + name + "\n",
        ( smaller[name]
          [["dept","muni",money_column,"item code"]] .
          sort_values( ["dept","muni","item code"] ) ) )
      print(
        "\AGGREGATED: " + name_of_data_source + ": " + name + "\n",
        ( smaller[name]
          [["dept","muni",money_column,"item code"]] .
          groupby( [ "dept","muni","item code" ] ) .
          agg( sum ) .
          reset_index() .
          sort_values( ["dept","muni","item code"] )
          [["dept","muni",money_column,"item code"]] ) )

