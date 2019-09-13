if True:
  import pandas as pd
  import numpy as np
  #
  import Code.build.classify_budget_codes as codes
  import Code.build.use_keys as uk
  import Code.integ_tests.integ_util as iu
  import Code.series_metadata as ser

name_of_data_source = "budget_7_verbose"

if True: # build data
  s7_dfs = {} # the input data
  smaller = {} # a spacetime subset of that input data
  for name in ["ingresos","gastos"]:
    df = pd.read_csv(
        "output/" + name_of_data_source + "/recip-1/" + name + ".csv",
        encoding = "utf-8" )
    print( len(df) )
    s7_dfs[name] = df.copy()
    df["item categ"] = ( df["item categ"] .
                         apply( lambda x: x[0:20] ) )
    df = (
      df
      [   ( df["year"] == iu.year )
        & (   (               df["muni"] == iu.muni )
            | (   ( "dept" == df["muni"] )
                & (           df["dept"] == iu.dept ) ) ) ] )
    smaller[name] = df

if True: # report
  for (name,money_column) in [
      ("ingresos","item recaudo"),
      ("gastos","item oblig") ]:
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
        # This line is useful when comparing against earlier products.
          # sort_values( ["dept","muni","item categ"] ) ) )
        # The next two lines are useful when comparing against later ones.
          sort_values( ["dept","muni",money_column],
                       ascending = False ) ) )

