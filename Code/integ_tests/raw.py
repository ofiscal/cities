# This prints some data useful for eyballing against results
# at any stage of the build process.

if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict
  #
  import Code.common as c
  import Code.sample_tables_defs as st
  import Code.series_metadata as ser
  import Code.sample_tables_defs as defs
  import Code.build.classify_budget_codes as codes


if True: # get 2018 data
  common = { "Nombre DANE Departamento" : "dept",
             "Nombre DANE Municipio" : "muni",
             "Código Concepto" : "item code" }
  raw_2018 = "data/sisfut/original_csv/2018_"
  def grab( filename: str,
                money_column: str
              ) -> pd.DataFrame:
    return st.geo_select(
      pd.read_csv( raw_2018 + filename + ".csv",
                   usecols = list(common.keys()) + [money_column] ) .
      rename( columns = dict( common, **{money_column:"money"} ) ) )
  ing = grab( "ingresos", "Recaudo" )
  inv = grab( "inversion", "Obligaciones" )
  fun = grab( "funcionamiento", "Obligaciones" )

if True: # for taxes, compare the output to this
  ing2 = (ing[ ing["item code"] .
               isin( codes.of_interest["ingresos"] ) ] )
  ing2 = ing2[ (ing2["muni"] == "SANTA MARTA") |
               (ing2["dept"] == "ANTIOQUIA") ]
  print( "\nRAW DATA:" )
  ing2 . sort_values( ["dept","muni","item code"] )

