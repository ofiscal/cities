###### PURPOSE:
###### WHereas the last stage just collected those observations across years,
###### this one cleans them --
###### changing formats, filling missing values with 0
###### -- and tests the results.
###### The unit of observation is the same, a "budget",
###### i.e. an item of either expenditure (many, small) or income (few, big).

if True:
  import os
  import pandas as pd
  #
  import Code.build.budget_1_tests as tests
  import Code.common as common
  import Code.metadata.raw_series as raw
  import Code.metadata.terms as t
  import Code.util.misc as util


if True: # input data
  source = os.path.join ( common.outdata, "budget_0_collect" )
  dfs = {}
  for s in raw.series:
    dfs[s] = pd.read_csv (
      os.path.join ( source,
                     s + ".csv" ) )

if True: # format
  for s in raw.series:
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
  dest = os.path.join ( common.outdata, "budget_1" )
  if not os.path.exists( dest ):
    os.makedirs( dest )
  for s in raw.series:
    dfs[s].to_csv( dest + "/" + s + ".csv",
                   index = False )
