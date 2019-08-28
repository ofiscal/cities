###### Based on the original three data sets from DNP
###### (ingreso, inversiones and funcionamiento), this builds three
###### similar data sets.
###### The unit of observation is the same, a "concepto",
###### i.e. an item of either expenditure or income.
###### Some new columns are added --
###### namely "year", "subcode" and "code=subcode".
###### Some verbose, redundant columns are omitted.

import pandas as pd

import Code.build.conceptos_1_defs as defs
import Code.build.conceptos_1_tests as tests
import Code.build.sisfut_metadata as sm


dfs = defs.collect_raw( sm.source_folder + "original_csv" )

tests.row_numbers_raw( dfs )
tests.column_names_of_raw_data( dfs )
tests.types_and_missings_for_raw_data( dfs )

# compute aggregated item code (ic) columns
dfs_ic = defs.aggregated_item_codes( dfs )
tests.row_numbers_after_keeping_only_relevant_item_codes( dfs_ic )
tests.column_names_after_agg( dfs_ic )
tests.types_and_missings_for_data_after_adding_item_code_columns( dfs_ic )

for s in sm.series:
  dfs_ic[s].to_csv( "output/conceptos_1/" + s + ".csv",
                    index = False )
