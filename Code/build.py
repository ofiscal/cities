from itertools import chain
import numpy as np
import pandas as pd
import Code.sisfut_about as sc


######
###### Build "concepto" data
###### These are the data sets "ingresos", "inversion", and "funcionamiento",
###### collecting across years and dropping verbose duplicative columns.
###### The unit of observation is a "concepto",
###### i.e. an item of either expenditure or income.
######

dfs = {}
for series in sc.series:
  dfs[series] = pd.DataFrame()
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv(
      ( sc.source_folder + "original_csv/"
        + str(year) + "_" + series + ".csv" )
      , usecols = set.difference(
          set( sc.column_subsets[series] )
        , sc.omittable_columns ) # omit the verbose, redundant columns
    )
    shuttle["year"] = year
    dfs[series] = dfs[series] . append(shuttle)
  dfs[series] . to_csv( "output/trimmed_transfers/" + series + ".csv"
                      , index = False )
