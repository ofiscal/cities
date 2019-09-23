# This prints some data useful for eyballing against results
# at any stage of the build process.

if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict
  #
  import Code.build.classify_budget_codes as codes
  import Code.common as c
  import Code.integ_tests.integ_util as iu
  import Code.util.aggregate_all_but_biggest as defs
  import Code.metadata.two_series as ser


name_of_data_source = "raw data"

if True: # get 2018 data
  col_map = { "Nombre DANE Departamento" : "dept",
             "Nombre DANE Municipio" : "muni",
             "Código Concepto" : "item code" }
  raw_yr = "data/sisfut/original_csv/" + str( iu.year ) + "_"
    # PITFALL: This is neither file nor folder,
    # but rather the common prefix of some files.
  def grab( filename: str,
                money_column: str
              ) -> pd.DataFrame:
    df = (
      pd.read_csv( raw_yr + filename + ".csv",
                   usecols = list(col_map.keys()) + [money_column] ) .
      rename( columns = dict( col_map, **{money_column:"money"} ) ) )
    df["muni"] = df["muni"].fillna(-1)
    return df[["dept","muni","money","item code"]]
  ing = grab( "ingresos", "Recaudo" )
  inv = grab( "inversion", "Obligaciones" )
  fun = grab( "funcionamiento", "Obligaciones" )

smaller,agged = {},{}
for (name,df) in [
    ("ingresos"       ,ing.copy()),
    ("inversion"      ,inv.copy()),
    ("funcionamiento" ,fun.copy())
    ]:
  df = ( df[ df["item code"] .
             isin( codes.of_interest[name] ) ] )
  df = df[ (         df["muni"] == iu.muni )
             | (   ( df["muni"] == -1 )
                 & ( df["dept"] == iu.dept) ) ]
  smaller[name] = df
  agged[name] = ( df . groupby( [ "dept","muni","item code" ] ) .
                  agg( sum ) .
                  reset_index() )

if True: # find a muni that aggregates edu or infra codes
  edu_or_infra = {}
  for (name,src) in [("inversion",inv),
               ("funcionamiento",fun)]:
    df = src.copy()
    df["one"] = 1
    df = df[ df["item code"] .
             isin( set.union(
                     codes.categs_to_code_sets[codes.edu],
                     codes.categs_to_code_sets[codes.infra] ) ) ]
    df = ( df . groupby( ["muni","dept","item code"] ) .
           agg( sum ) . reset_index() )
    edu_or_infra[name] = df
    # The inversion data has, for all space cells in 2014,
    # no rows with duplicate item codes. For the funcionamiento data,
    # muni ARACATACA and dept SANTANDER (and some others) *do*
    # have duplicate education codes -- e.g. 1.3.6.1.1.
    # Run the following to see the preceding.
    # >>> x = edu_or_infra["funcionamiento"]
    # >>> x[ x["one"] > 1 ]

for name in ["ingresos","inversion","funcionamiento"]:
  print(
    "\DISAGGREGATED: " + name_of_data_source + ": " + name + "\n",
    smaller[name] . sort_values( ["dept","muni","item code"] ) )
  print(
    "\AGGREGATED: " + name_of_data_source + ": " + name + "\n",
    agged[name] .   sort_values( ["dept","muni","item code"] ) .
    reset_index()
    [["dept","muni","money","item code"]]
  )

