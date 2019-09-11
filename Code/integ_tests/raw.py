# This prints some data useful for eyballing against results
# at any stage of the build process.

if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict
  #
  import Code.common as c
  import Code.integration_tests.integ_util as iu
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
    return iu.geo_select(
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

if True:
  assert "look at gastos (disabled codebelow)" == "done"
  assert "look at regalias" == "done"
  assert "Use places where multiple funcionamiento codes are summed for infrastructure spending" == "done"
  assert "Use years that require deflation" == "done"

if False: # construct some test data with those codes
  for cs in [iu.edu_codes, iu.infra_codes]:
    inv2 = (inv[ inv["item code"] .
                 isin( cs ) ] )
    fun2 = (fun[ fun["item code"] .
                 isin( cs ) ] )
    gastos = pd.concat( [inv2, fun2], axis = "rows" )
    ( gastos
      [(gastos["muni"] == "SANTA MARTA") |
       (gastos["dept"] == "ANTIOQUIA") ] .
      sort_values( ["dept","muni","item code"] ) )

