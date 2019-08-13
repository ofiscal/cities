###### Based on the original three data sets from DNP
###### (ingreso, inversiones and funcionamiento), this builds three
###### similar data sets.
###### The unit of observation is the same, a "concepto",
###### i.e. an item of either expenditure or income.
###### Some new columns are added --
###### namely "year", "subcode" and "code=subcode".
###### Some verbose, redundant columns are omitted.

from itertools import chain
import numpy as np
import pandas as pd
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


######
###### Build "concepto" data
######
# These are the data sets "ingresos", "inversion", and "funcionamiento",
# collecting across years and dropping verbose duplicative columns.

dfs = {}
for series in sm.series:
  dfs[series] = pd.DataFrame()
  for year in range( 2012, 2018+1 ):
    shuttle = (
      pd.read_csv(
        ( sm.source_folder + "original_csv/"
          + str(year) + "_" + series + ".csv" )
#        , nrows = 20000
        , usecols = set.difference(
            set( sm.column_subsets_long[series] )
          , sm.omittable_columns_long ) ) . # omit the omittable ones
      rename( columns = dict( sm.column_subsets[series] ) ) )
    shuttle["year"] = year
    dfs[series] = dfs[series] . append(shuttle)


######
###### Build aggregated concepto-code columns.
######
# This does not aggregate rows; it merely builds the aggregate subcodes
# by which the data will be (in the next program) aggregated.

for (series, regexes) in [
      ("inversion"      , ac.regexes_for_2_codes() )
    , ("funcionamiento" , ac.regexes_for_2_codes() )
    , ("ingresos"       , ac.regexes_for_ingresos() ) ]:
  df = dfs[series]

  # build some columns
  (category, top, child) = regexes
  df["item categ"]       = (
      df["item code"]
    . str.extract( category ) )
  df["item top"]   = ~ pd.isnull(
      df["item code"]
    . str.extract( top ) )
  df["item child"] = ~ pd.isnull(
      df["item code"]
    . str.extract( child ) )

  df = ( # keep only rows labeled with top categories
         # or the first generation below the top categories
    df[ (df["item top"])
      | (df["item child"]) ] )

  # Verify that codigo-top is the boolean negative of codigo-child.
  # (That's not true before we drop rows categorized deeper than top or child.)
  assert ( len ( df[ ( (df["item top"].astype(int)) +
                       (df["item child"]).astype(int) )
                     != 1 ] )
           == 0 )
  df = df.drop( columns = ["item child"] )

  df . to_csv( "output/conceptos_1/" + series + ".csv"
             , index = False )
  dfs[series] = df
