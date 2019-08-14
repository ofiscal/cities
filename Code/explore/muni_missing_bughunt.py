# This mimics conceptos_1.py.
# By the end of it, both dfs and efs yield missing-fractions less than 1.
# raw is also well behaved -- but somehow dfs1 has a fraction of 1.

import numpy as np
import pandas as pd

import Code.build.sisfut_metadata as sm
import Code.explore.muni_missing_5_percent as miss
import Code.build.conceptos_1_defs as defs


def analyze( dfs, colname ):
  for s in sm.series:
    print(s)
    df = dfs[s]
    df_bad = df[ df[colname] .isnull() ]
    print( len(df_bad) / len(df) )

dfs = defs.collect_raw()
analyze(dfs, "muni code")

dfs2 = defs.aggregated_item_codes( dfs )
analyze(dfs2, "muni code")

if False: # write data
  for s in sm.series:
    dfs2[s].to_csv( "output/conceptos_1/" + s + ".csv",
                    index = False )

if True: # read data
  dfs3 = {}
  for s in sm.series:
    df = pd.read_csv( "output/conceptos_1/" + s + ".csv" )
    dfs3[s] = df
  analyze(dfs3, "muni code")
