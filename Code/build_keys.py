from itertools import chain
import pandas as pd
import Code.sisfut_about as sc


source_data = pd.DataFrame()
for series in sc.series:
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv(
      ( sc.source_folder + "original_csv/"
        + str(year) + "_" + series + ".csv" )
      , usecols = [
          "Cód. DANE Municipio"
        , "Nombre DANE Municipio"
        , "Nombre DANE Departamento"
        , "Código Concepto"
        , "Concepto"
      ] )
  source_data = source_data.append( shuttle )

def make_key( from_columns, to_columns, df ):
  return ( df[ list( chain.from_iterable(
                      [from_columns, to_columns] ) ) ]
         . groupby( from_columns )
         . agg( lambda x: x.iloc[0] ) # take the first in each to_column
         . reset_index() )

( make_key(
      ["Cód. DANE Municipio"]
    , [ "Nombre DANE Municipio"
      , "Nombre DANE Departamento" ]
    , source_data )
  . to_csv(
      "output/keys/geo.csv"
    , index = False ) )

( make_key(
      [ "Código Concepto" ]
    , [ "Concepto" ]
    , source_data )
  . to_csv(
      "output/keys/concepto.csv"
    , index = False ) )
