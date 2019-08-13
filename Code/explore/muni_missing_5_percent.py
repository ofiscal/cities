# Demonstrates that 3% to 5% of observations in each data set
# are missing both municipality (name) and municipality code.
 itertools import chain
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
        , usecols = [ "Cód. DANE Municipio",
                      "Nombre DANE Municipio" ] ) .
      rename( columns = dict( sm.column_subsets[series] ) ) )
    shuttle["year"] = year
    dfs[series] = dfs[series] . append(shuttle)

for s in sm.series:
  print(s)
  df = dfs[s]
  df_bad = df[
    ( df["muni code"] .isnull() ) &
    ( df["muni"]      .isnull() ) ]
  print( len(df_bad) / len(df) )
