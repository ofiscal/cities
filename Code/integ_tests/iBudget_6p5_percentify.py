if True:
  import pandas as pd
  import numpy as np
  #
  import Code.build.classify_budget_codes as codes
  import Code.build.use_keys as uk
  import Code.integ_tests.integ_util as iu
  import Code.metadata.four_series as s4

name_of_data_source = "budget_6p5_cull_and_percentify"

if True: # build data
  s6p5_dfs = {} # the input data
  smaller = {} # a spacetime subset of that input data
  for s in s4.series:
    name = s.name
    df = uk.merge_geo(
      pd.read_csv( "output/" + name_of_data_source +
                   "/recip-1/" + name + ".csv" ) )
    s6p5_dfs[name] = df.copy()
    df["item categ"] = ( df["item categ"] .
                         apply( lambda x: x[0:20] ) )
    df = (
      df
      [   ( df["year"] == iu.year )
        & (   (                df["muni"] == iu.muni )
            | (   ( pd.isnull( df["muni"] ) )
                & (            df["dept"] == iu.dept ) ) ) ] )
    df["muni"] = df["muni"].fillna(-1)
    smaller[name] = df

if True: # report
  for (name,money_column) in [
      ("ingresos"     ,"item total"),
      ("ingresos-pct" ,"item total"),
      ("gastos"       ,"item oblig"),
      ("gastos-pct"   ,"item oblig") ]:
    print(
      "\DISAGGREGATED: " + name_of_data_source + ": " + name + "\n",
      ( smaller[name]
        [["dept","muni",money_column,"item categ"]] .
        sort_values( ["dept","muni","item categ"] ) ) )
    print(
      "\AGGREGATED: " + name_of_data_source + ": " + name + "\n",
      ( smaller[name] .
        groupby( [ "dept","muni","item categ" ] ) .
        agg( sum ) .
        reset_index()
        [["dept","muni",money_column,"item categ"]] .
        sort_values( ["dept","muni","item categ"] ) ) )

if True: # report on averages in a few categories
  for (name,categ) in [
      ("ingresos-pct" ,"Por recursos propios"),
      ("gastos-pct"   ,"Salud") ]:
    df = s6p5_dfs[name].copy()
    df = ( df
           [ ( df["item categ"] == categ ) &
             ( df["year"] == iu.year ) &
             ( df["dept"] == iu.dept ) ] )
    if name == "ingresos-pct":
      df = df.drop( columns = ["muni","dept"] )
    print(
      "ALL MUNIS, " + categ + " only: " + name_of_data_source + ": " + name + "\n",
      df )

