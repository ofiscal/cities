###### This step takes so long that it deserves to be in its own file.

if True:
  import os
  import pandas as pd
  #
  import Code.build.budget_1_defs as defs
  import Code.metadata.raw_series as raw

if True:
  dest = "output/budget_0_collect"
  if not os.path.exists( dest ):
    os.makedirs(         dest )

dfs = defs.collect_raw( raw.source_folder + "csv" )

for s in raw.series:
  dfs[s].to_csv( dest + "/" + s + ".csv",
                 index = False )

