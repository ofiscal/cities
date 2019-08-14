import os

import Code.build.conceptos_2_subsample_defs as defs
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

for subsample in [10,100,1000]:
  if not os.path.exists( defs.sub_dest( subsample ) ):
    os.makedirs(         defs.sub_dest( subsample ) )
  munis_subset = defs.munis_subset( subsample,
                                    munis )
  dfs_subset   = defs.dfs_subset( munis_subset,
                                  dfs )
  for s in sm.series:
    dfs_subset[s].to_csv(
      defs.sub_dest( subsample ) + "/" + s + ".csv",
      index = False )

