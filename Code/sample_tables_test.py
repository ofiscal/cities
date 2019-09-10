if True:
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.series_metadata as ser
  import Code.sample_tables_defs as defs


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


if True:
  assert "Resume here" == False
