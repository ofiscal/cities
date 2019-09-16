# This mimics budget_1.py.
# By the end of it, both dfs and efs yield missing-fractions less than 1.
# raw is also well behaved -- but somehow dfs1 has a fraction of 1.

import numpy as np
import pandas as pd

import Code.metadata.three_series            as sm
import Code.build.budget_1_defs           as d1
import Code.build.budget_2_subsample_defs as d2


def analyze( dfs, colname ):
  for s in sm.series:
    print(s)
    df = dfs[s]
    df_bad = df[ df[colname] .isnull() ]
    print( len(df_bad) / len(df) )


######
###### (mostly) duplicating the code from
###### budget_2_subsample.py
######

dfs   = d2.read_data( nrows = 20000 )
analyze( dfs, "muni code" ) # so far, so good
munis = d2.munis_unique( dfs )

### <<< The problem was here.
for subsample in [10]:
  munis_subset = d2.subsample( subsample,
                               munis )
  dfs_subset   = d2.dfs_subset( munis_subset,
                                dfs )
  analyze( dfs_subset, "muni code" )

munis = pd.Series()
for s in sm.series:
  print( dfs[s]["muni code"] )
## The problem was here >>>

if True: # reading from what it writes to disk
  dfs3 = {}
  for s in sm.series:
    df = pd.read_csv( "output/budget_2_subsample/recip-10/" + s + ".csv" )
    dfs3[s] = df
    print( len( df ) )
  analyze(dfs3, "muni code")


######
###### (mostly) duplicating the code from
###### budget_1.py
######

if False: # everything but writing to disk
  dfs = d1.collect_raw()
  analyze(dfs, "muni code")
  dfs2 = d1.aggregated_item_codes( dfs )
  analyze(dfs2, "muni code")

if False: # writing to disk
  for s in sm.series:
    dfs2[s].to_csv( "output/budget_1/" + s + ".csv",
                    index = False )

if True: # reading from what it writes to disk
  dfs3 = {}
  for s in sm.series:
    df = pd.read_csv( "output/budget_1/" + s + ".csv" )
    dfs3[s] = df
  analyze(dfs3, "muni code")

