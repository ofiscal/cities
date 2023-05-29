# PURPOSE: Subsample the municipalities.
# Every subsample must have all the departments,
# which makes the dataflow a bit complex --
# we test that the sample size shrank by roughly a factor of 10
# (100, 1000) in the municipalities alone,
# then add departments back in just before writing to disk.

if True:
  from typing import Dict,Set,List
  import os
  import pandas as pd
  import numpy as np
  #
  import Code.build.budget_2_subsample_defs as defs
  import Code.build.use_keys as uk
  import Code.metadata.two_series as s2


if not os.path.exists( defs.top_dest ):
  os.makedirs( defs.top_dest )

# For the recip-1/ folder, use a symlink; don't copy the full sample.
if True:
  # PITFALL: The following uses absolute paths.
  # It's hard to do otherwise, because the destination folder
  # is different from the working folder.
  # PITFALL: "lexists" is not a typo. It differs from "exists"
  # in that "lexists" returns True for broken symlinks,
  # whereas "exists"  returns False.
  abs_recip_1_folder = os.path.join ( defs.home, defs.sub_dest(1) )
  abs_source         = os.path.join ( defs.home, defs.source )
  if os.path.lexists(     abs_recip_1_folder ):
    os.remove(            abs_recip_1_folder )
  os.symlink( abs_source, abs_recip_1_folder )

if True:
  dfs = defs.read_data()
  munis_df = uk.geo[["dept code","muni code"]]
  depts_df = uk.depts[["dept code"]]
  depts_df["muni code"] = 0

for subsample in [1000, 100, 10]: # smallest first, to catch errors faster
  if not os.path.exists( defs.sub_dest( subsample ) ):
    os.makedirs(         defs.sub_dest( subsample ) )
  if True: # build `places` : Set[ (dept code, muni code) ]
    munis_df_subsample = defs.subsample( subsample,
                                         munis_df )
    depts_df_subsample = defs.subsample(
      min(subsample,30), # to ensure there is at least one
      depts_df )
    places = pd.concat( [
        munis_df_subsample,
        depts_df_subsample ] )
  for s in s2.series:
    df = dfs[s.name]
    df = df.merge( places,
                   on = ["dept code","muni code"],
                   how = "inner" )
    df . to_csv (
      os.path.join ( defs.sub_dest ( subsample ),
                     s.name + ".csv" ),
      index = False )
