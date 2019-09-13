# Subsample municipalities.
# Every subsample will, however, have all the departments.
# The required testing of lengths makes the dataflow a bit complex --
# we test that the sample size shrank by roughly a factor of 10
# (100, 1000) in the municipalities alone,
# then add departments back in just before writing to disk.

if True:
  import os
  import pandas as pd
  import numpy as np
  
  import Code.build.budget_1p5_tests as test
  import Code.build.budget_2_subsample_defs as defs
  import Code.series_metadata as ser

if not os.path.exists( defs.top_dest ):
  os.makedirs( defs.top_dest )

# For the recip-1/ folder, use a symblink; don't copy the full sample.
if True:
  if os.path.exists(       defs.sub_dest(1) ):
    os.remove(             defs.sub_dest(1) )
  os.symlink( defs.source, defs.sub_dest(1) )

dfs                = defs.read_data()
dfs_muni, dfs_dept = {},{}
for s in ser.series: # deep copy
  sn = s.name
  dfs_muni[sn] = dfs[sn] [~pd.isnull( dfs[sn]["muni code"] ) ] . copy()
  dfs_dept[sn] = dfs[sn] [ pd.isnull( dfs[sn]["muni code"] ) ] . copy()
  assert len(dfs[sn]) == len(dfs_muni[sn]) + len(dfs_dept[sn])

munis = defs.munis_unique_without_nan( dfs )
assert (len(munis) < 1150) & (len(munis) > 1050)
del(dfs)

for subsample in [1000,100,10]: # smallest first, to catch errors faster
  if not os.path.exists( defs.sub_dest( subsample ) ):
    os.makedirs(         defs.sub_dest( subsample ) )
  muni_code_subsample = defs.subsample( subsample,
                                    munis )
  dfs_muni_subset   = defs.dfs_subset( muni_code_subsample,
                                       dfs_muni )
  test.column_names_after_agg( ["ingresos","gastos"],
                               dfs_muni_subset )
  for s in ["ingresos","gastos"]:
    # Test that the length of each subsample is reasonable.
    # The 1/10 subsample, for instance, should be not less than half,
    # and not more than twice, len(df) / 10.
    # It's not exact because some cities have more budget items recorded than others.
    df    = dfs_muni       [s]
    dfsub = dfs_muni_subset[s]
    assert ( ( 2 *   len(df) / subsample )
             >=      len(dfsub) )
    assert ( ( 0.5 * len(df) / subsample )
             <=      len(dfsub) )
  for s in ["ingresos","gastos"]:
    ( ( dfs_muni_subset[s] .
        append( dfs_dept[s] ) ) .
    to_csv(
      defs.sub_dest( subsample ) + "/" + s + ".csv",
      encoding="utf-8",
      index = False ) )
