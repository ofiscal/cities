###### Based on the original three data sets from DNP
###### (ingresos, inversiones and funcionamiento), this builds three
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
    shuttle = pd.read_csv(
      ( sm.source_folder + "original_csv/"
        + str(year) + "_" + series + ".csv" )
#      , nrows = 20000
      , usecols = set.difference(
          set( sm.column_subsets[series] )
        , sm.omittable_columns ) ) # omit the verbose, redundant columns
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
  (category, top, child) = regexes
  df["codigo"]       = (
      df["Código Concepto"]
    . str.extract( category ) )
  df["codigo-top"]   = ~ pd.isnull(
      df["Código Concepto"]
    . str.extract( top ) )
  df["codigo-child"] = ~ pd.isnull(
      df["Código Concepto"]
    . str.extract( child ) )
  df = ( # keep only top categories and the first generation below
    df[ (df["codigo-top"])
      | (df["codigo-child"]) ] )
  df . to_csv( "output/conceptos_1/" + series + ".csv"
             , index = False )
  dfs[series] = df
