# # PURPOSE
###########
# These two files define two sets of codes:
#
# ## `geo.csv`
##############
#
# maps 5-digit geo codes to municipality names,
# and (redundantly, since each row is a municipality)
# 2-digit department codes to department names.
#
# ## `budget.csv`
#################
#
# maps budget codes to budget item names.
#
# ### How to interpret budget codes
###################################
#
# The codes look like `TI` or `A.10.19.1` or `1.2` --
# they can be any number of (.)-separated expressions,
# where the first might be alphabetical or numeric,
# and the rest are always numeric.
#
# If item X has a code with one fewer (.) than the code of item Y,
# it is because X is a linear combination of all such Ys.
# (I don't remember if X is always a simple sum,
# or if sometimes one subtracts rather than adding.)
# So for instance, item 1 = "TOTAL GASTOS DE FUNCIONAMIENTO"
# includes item 1.1 = "GASTOS DE PERSONAL".

if True:
  from   itertools import chain
  import os
  import pandas                    as pd
  #
  import Code.common               as common
  import Code.metadata.raw_series  as sm
  import Code.metadata.terms       as t


if True: # build source data set, from which both keys are built
  source_data = pd.DataFrame()
  for series in set.difference( {*sm.series},
                                {t.deuda} ):
    for year in range( 2013, common.last_year + 1 ):
      filepath = (
        os.path.join (
          common.indata,
          "sisfut", "csv",
          str(year) + "_" + series + ".csv" ) )
      shuttle = pd.read_csv (
        filepath,
        usecols = [
           "Cód. DANE Municipio",
           "Nombre DANE Municipio",
           "Cód. DANE Departamento",
           "Nombre DANE Departamento",
           "Código Concepto",
           "Concepto"
         ] )
      source_data = pd.concat( [ source_data, shuttle ] )

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

dest = os.path.join ( common.outdata, "keys" )
if not os.path.exists( dest ):
  os.makedirs ( dest )

( make_key ( [ "Cód. DANE Municipio" ],
             [ "Nombre DANE Municipio",
               "Cód. DANE Departamento",
               "Nombre DANE Departamento" ],
             source_data )
  . to_csv ( os.path.join ( dest, "geo.csv" ),
             index = False ) )

( make_key ( [ "Código Concepto" ],
             [ "Concepto" ],
             source_data )
  . to_csv ( os.path.join ( dest, "budget.csv" ),
             index = False ) )
