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
  import Code.sample_tables_defs as defs
  import Code.sample_tables_defs as st
  import Code.series_metadata as ser


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
    df = st.geo_select(
      pd.read_csv( raw_yr + filename + ".csv",
                   usecols = list(col_map.keys()) + [money_column] ) .
      rename( columns = dict( col_map, **{money_column:"money"} ) ) )
    df["muni"] = df["muni"].fillna(-1)
    return df
  ing = grab( "ingresos", "Recaudo" )
  inv = grab( "inversion", "Obligaciones" )
  fun = grab( "funcionamiento", "Obligaciones" )

smaller = {}
for (name,source) in [
    ("ingresos",ing),
    ("inversion",inv),
    ("funcionamiento",fun)
    ]:
  df = ( source[ source["item code"] .
                 isin( codes.of_interest[name] ) ] )
  df = ( df[ (df["muni"] == iu.muni) |
             (df["dept"] == iu.dept) ] )
  smaller[name] = df
  print(
    "\DISAGGREGATED: " + name_of_data_source + ": " + name + "\n",
    df . sort_values( ["dept","muni","item code"] ) )
  print(
    "\AGGREGATED: " + name_of_data_source + ": " + name + "\n",
    ( df . groupby( [ "dept","muni","item code" ] ) .
      agg( sum ) .
      sort_values( ["dept","muni","item code"] ) ) )


