# This mimics conceptos_1.py.
# By the end of it, both dfs and efs yield missing-fractions less than 1.
# raw is also well behaved -- but somehow dfs1 has a fraction of 1.

import numpy as np
import pandas as pd

import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm
# import Code.explore.muni_missing_5_percent as miss


######
###### The first part of build/conceptos_1
######

dfs = {}
for series in sm.series:
  dfs[series] = pd.DataFrame()
  for year in range( 2012, 2018+1 ):
    shuttle = (
      pd.read_csv(
        ( sm.source_folder + "original_csv/"
          + str(year) + "_" + series + ".csv" )
        , nrows = 20000
        , usecols = set.difference(
            set( sm.column_subsets_long[series] )
          , sm.omittable_columns_long ) ) . # omit the omittable ones
      rename( columns = dict( sm.column_subsets[series] ) ) )
    shuttle["year"] = year
    dfs[series] = dfs[series] . append(shuttle)

######
###### Tests, which fail.
######

def analyze( dfs, colname ):
  for s in sm.series:
    print(s)
    df = dfs[s]
    df_bad = df[ df[colname] .isnull() ]
    print( len(df_bad) / len(df) )

analyze(dfs, "muni code")
