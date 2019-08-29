import os

from Code.build.budget_1_tests import column_names_after_agg
import Code.build.budget_2_subsample_defs as defs
import Code.build.sisfut_metadata as sm


if not os.path.exists( defs.top_dest ):
  os.makedirs( defs.top_dest )

# For the recip-1/ folder, use a symblink; don't copy the full sample.
if True:
  if os.path.exists(       defs.sub_dest(1) ):
    os.remove(             defs.sub_dest(1) )
  os.symlink( defs.source, defs.sub_dest(1) )

dfs   = defs.read_data()
munis = defs.munis_unique( dfs )

for subsample in [1000,100,10]: # smaller ones first, to catch errors faster
  if not os.path.exists( defs.sub_dest( subsample ) ):
    os.makedirs(         defs.sub_dest( subsample ) )
  munis_subsample = defs.subsample( subsample,
                                    munis )
  dfs_subset   = defs.dfs_subset( munis_subsample,
                                  dfs )
  column_names_after_agg( dfs_subset )
  for s in sm.series:
    df        = dfs       [s]
    df_subset = dfs_subset[s]
    # Test that the length of each subsample is reasonable.
    # The 1/10 subsample, for instance, should be not less than half,
    # and not more than twice, len(df) / 10.
    # It's not exact because some cities have more budget items recorded than others.
    assert ( ( 2 *   len(df) / subsample )
             >=      len(df_subset) )
    assert ( ( 0.5 * len(df) / subsample )
             <=      len(df_subset) )
    df_subset . to_csv(
      defs.sub_dest( subsample ) + "/" + s + ".csv",
      encoding="utf-16",
      index = False )

