###### Based on the original three data sets from DNP
###### (ingreso, inversiones and funcionamiento), this builds three
###### similar data sets.
###### The unit of observation is the same, a "budget",
###### i.e. an item of either expenditure or income.

if True:
  import os
  import pandas as pd
  #
  import Code.util.misc as util
  import Code.build.budget_1_tests as tests
  import Code.metadata.raw_series as raw
  import Code.metadata.terms as t

if True: # input data
  source = "output/budget_0_collect"
  dfs = {}
  for s in raw.series:
    dfs[s] = pd.read_csv( source + "/" + s + ".csv" )

if True: # format
  for s in [ t.ingresos,
             t.inversion,
             t.funcionamiento,
             t.deuda]:
    dfs[s] = (
      util.un_latin_decimal_columns(
        list( map( lambda pair: pair[1],
                   raw.columns_peso[s] ) ),
        dfs[s] ) .
      fillna(0) )
    dfs[s]["muni code"] = (
      dfs[s]["muni code"] .
      fillna(0) )

if True: # test
  tests.row_numbers_raw( dfs )
  tests.column_names_of_raw_data( dfs )
  tests.types_and_missings_for_raw_data( dfs )

if True: # write
  dest = "output/budget_1"
  if not os.path.exists( dest ):
    os.makedirs( dest )
  for s in raw.series:
    dfs[s].to_csv( dest + "/" + s + ".csv",
                   index = False )

