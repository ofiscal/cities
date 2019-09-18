###### Based on the original three data sets from DNP
###### (ingreso, inversiones and funcionamiento), this builds three
###### similar data sets.
###### The unit of observation is the same, a "budget",
###### i.e. an item of either expenditure or income.

if True:
  import os
  import pandas as pd
  #
  import Code.util as util
  import Code.build.budget_1_defs as defs
  import Code.build.budget_1_tests as tests
  import Code.metadata.four_series as sm
  import Code.metadata.terms as t

dfs = defs.collect_raw( sm.source_folder + "original_csv" )
dfs[t.deuda] = util.un_latin_decimal_columns(
  list( map( lambda s: s[1],
             sm.columns_peso[t.deuda] ) ),
  dfs[t.deuda] )

tests.row_numbers_raw( dfs )
tests.column_names_of_raw_data( dfs )
tests.types_and_missings_for_raw_data( dfs )

dest = "output/budget_1"
if not os.path.exists( dest ):
  os.makedirs( dest )
for s in sm.series:
  dfs[s].to_csv( dest + "/" + s + ".csv",
                 index = False )

