if True:
  import os
  from itertools import chain
  import pandas as pd
  import Code.metadata.terms as t
  import Code.metadata.raw_series as sm


if True: # build source data set, from which both keys are built
  source_data = pd.DataFrame()
  for series in set.difference(
      set(sm.series), set([t.deuda])):
    for year in range( 2013, 2018+1 ):
      filename = ( sm.source_folder + "csv/"
                   + str(year) + "_" + series + ".csv" )
      shuttle = pd.read_csv(
        filename,
        usecols = [
           "Cód. DANE Municipio",
           "Nombre DANE Municipio",
           "Cód. DANE Departamento",
           "Nombre DANE Departamento",
           "Código Concepto",
           "Concepto"
         ] )
      source_data = source_data.append( shuttle )

# PITFALL: If any tuple of keys in from_columns maps to more than one
# tuple in to_columns, make_key will only provide the first mapping it encounters.
# Thanks to the results from bijectivity_test.py,
# we know this loss of information happens in only one place:
# The "Código Concepto" value "VAL" maps to three distinct "Concepto" values.
# None of them are of interest, so it doesn't matter.
def make_key( from_columns, to_columns, df ):
  return ( df[ list( chain.from_iterable(
                      [from_columns, to_columns] ) ) ]
         . groupby( from_columns )
         . agg( lambda x: x.iloc[0] ) # take the first in each to_column
         . reset_index() )

if not os.path.exists( "output/keys" ):
  os.makedirs( "output/keys" )

( make_key(
      ["Cód. DANE Municipio"]
    , [ "Nombre DANE Municipio"
      , "Cód. DANE Departamento"
      , "Nombre DANE Departamento" ]
    , source_data )
  . to_csv(
    "output/keys/geo.csv",
    index = False ) )

( make_key(
      [ "Código Concepto" ]
    , [ "Concepto" ]
    , source_data )
  . to_csv(
    "output/keys/budget.csv",
    index = False ) )

