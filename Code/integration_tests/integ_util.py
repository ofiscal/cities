if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict

if True: # geo-narrowing a sample
  muni_sample = { "BOGOTÁ, D.C.",
                  "SANTA MARTA",
                  "FILANDIA",
                  "VALLE DEL GUAMUEZ" }

  dept_sample = { "ANTIOQUIA",
                  "CESAR",
                  "CHOCÓ",
                  "ARAUCA" }

  def geo_select( df : pd.DataFrame ) -> pd.DataFrame:
    return pd.concat(
      [ df[   df["muni"] .
              isin( muni_sample ) ],
        df[   pd.isnull(df["muni"] ) &
            ( df["dept"].isin( dept_sample ) ) ] ],
      axis = "rows" )

def get_2018_data() -> List[ pd.DataFrame ]:
  common = { "Nombre DANE Departamento" : "dept",
             "Nombre DANE Municipio" : "muni",
             "Código Concepto" : "item code" }
  raw_2018 = "data/sisfut/original_csv/2018_"
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
  return [ing,inv,fun]

if False: # for spending, first determine which budget categories
          # have the fewest components
  for k in codes.categs_to_code_sets.keys():
    print( "\n" + k + ": " +
           str( categs_to_code_sets[k] ) )
  """ RESULT: Two good categories would be these:
  Infraestructura y vivienda: {'A.15', '1.3.11', 'A.7', 'A.9'}
  Educación: {'1.3.6.1.1', 'A.1', '1.3.6.4.1', '1.3.6.4.6'}
  One involves multiple inversion codes and one funcionamiento code,
  and the other the reverse. """

if True: # the codes discovered in the last section
  edu_codes = {'A.15', '1.3.11', 'A.7', 'A.9'}
  infra_codes = {'1.3.6.1.1', 'A.1', '1.3.6.4.1', '1.3.6.4.6'}
