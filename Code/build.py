from itertools import chain
import numpy as np
import pandas as pd
import Code.aggregate_concepto as ac
import Code.sisfut_about as sc
import time


######
###### Build "concepto" data
######
# These are the data sets "ingresos", "inversion", and "funcionamiento",
# collecting across years and dropping verbose duplicative columns.
# The unit of observation is a "concepto",
# i.e. an item of either expenditure or income.

dfs = {}
for series in sc.series:
  dfs[series] = pd.DataFrame()
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv(
      ( sc.source_folder + "original_csv/"
        + str(year) + "_" + series + ".csv" )
      , nrows = 1000
      , usecols = set.difference(
          set( sc.column_subsets[series] )
        , sc.omittable_columns ) ) # omit the verbose, redundant columns
    shuttle["year"] = year
    dfs[series] = dfs[series] . append(shuttle)
  dfs[series] . to_csv( "output/trimmed_transfers/" + series + ".csv"
                      , index = False )


######
###### Build aggregated concepto columns
######

subcode_function_map = [
    ("inversion"      , lambda x: ac.first_n_subcodes(2,x))
  , ("funcionamiento" , lambda x: ac.first_n_subcodes(2,x))
  , ("ingresos"       , ac.ingreso_subcodes) ]
start = time.time()
for (series, subcode_function) in subcode_function_map:
  df = dfs[series]
  df[["subcode","subcode ="]] = (
    df["Código Concepto"]
    . apply( lambda c:
             pd.Series(
               subcode_function( c ) ) ) )

end = time.time()
print( "duration in seconds: ", end - start )


######
###### Temporary diagnostics
######

ing = dfs["ingresos"]
inv = dfs["inversion"]
fun = dfs["funcionamiento"]

fun[[ "Código Concepto", "subcode", "subcode =" ]]
