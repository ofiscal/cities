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

subcode_regex_map = [
    ("inversion"      , ac.regex_for_at_least_n_codes(2) )
  , ("funcionamiento" , ac.regex_for_at_least_n_codes(2) )
  , ("ingresos"       , ac.ingreso_regex ) ]
for (series, subcode_regex) in subcode_regex_map:
  df = dfs[series]
  df["subcode"] = (
    df["Código Concepto"]
    . str.extract( subcode_regex ) )
  df["code=subcode"] = (
    df["Código Concepto"] == df["subcode"] )
  dfs[series] . to_csv( "output/conceptos_1/" + series + ".csv"
                      , index = False )
