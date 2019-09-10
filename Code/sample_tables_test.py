# These

if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict
  #
  import Code.common as c
  import Code.series_metadata as ser
  import Code.sample_tables_defs as defs
  import Code.build.classify_budget_codes as codes


if True: # Get raw 2018 data
  common = { "Nombre DANE Departamento" : "dept",
             "Nombre DANE Municipio" : "muni",
             "Código Concepto" : "item" }
  raw_2018 = "data/sisfut/original_csv/2018_"
  #
  def geo_select( df : pd.DataFrame ) -> pd.DataFrame:
    return pd.concat(
      [ df[ df["muni"].isin( { "BOGOTÁ, D.C.",
                               "SANTA MARTA",
                               "FILANDIA",
                               "VALLE DEL GUAMUEZ" } ) ],
        df[   pd.isnull(df["muni"] ) &
            ( df["dept"].isin( [ "ANTIOQUIA",
                                 "CESAR",
                                 "CHOCÓ",
                                 "ARAUCA" ] ) ) ] ],
      axis = "rows" )
  #
  def get_2018( filename: str,
                money_column: str
              ) -> pd.DataFrame:
    return geo_select(
      pd.read_csv( raw_2018 + filename + ".csv",
                   usecols = list(common.keys()) + [money_column] ) .
      rename( columns = dict( common, **{money_column:"money"} ) ) )
  ing = get_2018( "ingresos", "Recaudo" )
  inv = get_2018( "inversion", "Obligaciones" )
  fun = get_2018( "funcionamiento", "Obligaciones" )

if True: # for taxes, compare the output to this
  ing2 = (ing[ ing["item"] .
               isin( codes.of_interest["ingresos"] ) ] )
  ing2 = ing2[ (ing2["muni"] == "SANTA MARTA") |
               (ing2["dept"] == "ANTIOQUIA") ]
  ing2

if True: # for spending, first determine which budget categories
         # have the fewest components
  categs_to_code_sets = (
    codes.invert_many_to_one_dict( codes.codes_to_categs ) )
  for k in categs_to_code_sets.keys():
    pass
    # print( "\n" + k + ": " +
    #       str( categs_to_code_sets[k] ) )
  """ RESULT: Two good categories would be these:
  Infraestructura y vivienda: {'A.15', '1.3.11', 'A.7', 'A.9'}
  Educación: {'1.3.6.1.1', 'A.1', '1.3.6.4.1', '1.3.6.4.6'}
  One involves multiple inversion codes and one funcionamiento code,
  and the other the reverse. """
  edu_codes = {'A.15', '1.3.11', 'A.7', 'A.9'}
  infra_codes = {'1.3.6.1.1', 'A.1', '1.3.6.4.1', '1.3.6.4.6'}

if True: # construct some test data with those codes
  for cs in [edu_codes, infra_codes]:
    inv2 = (inv[ inv["item"] .
                 isin( cs ) ] )
    fun2 = (fun[ fun["item"] .
                 isin( cs ) ] )
    gastos = pd.concat( [inv2, fun2], axis = "rows" )
    ( gastos
      [(gastos["muni"] == "SANTA MARTA") |
       (gastos["dept"] == "ANTIOQUIA") ] .
      sort_values( ["muni","dept"] ) )

if True:
  assert "look at regalias" == "done"
  assert "Use places where multiple funcionamiento codes are summed for infrastructure spending" == "done"
  assert "Use years that require deflation" == "done"
