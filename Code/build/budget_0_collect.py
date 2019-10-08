###### This step takes so long that it deserves to be in its own file.
if True:
  import os
  from typing import Set
  import numpy as np
  import pandas as pd
  #
  import Code.metadata.raw_series as raw

if True:
  dest = "output/budget_0_collect"
  if not os.path.exists( dest ):
    os.makedirs(         dest )

def collect_raw( source : str,
                 extra_columns : Set[str] = set(),
                 **kwargs ):
  """Returns a dictionary of three data frames, one for each of ingresos, inversion and funcionamiento. If using the optional 'nrows' argument, bear in mind that the 3 data sets have about 4 million rows between them."""
  dfs = {}
  for series in raw.series:
    dfs[series] = pd.DataFrame()
    for year in range( 2013, 2018+1 ):
      shuttle = (
        pd.read_csv(
          source + "/" + str(year) + "_" + series + ".csv",
          usecols = set.union(
            extra_columns,
            set.difference(
              set( raw.column_subsets_long[series] ),
              raw.omittable_columns_long ) ), # omit the omittable ones
          **kwargs ) .
        rename( columns = dict( raw.column_subsets[series] ) ) )
      shuttle["year"] = year
      dfs[series] = dfs[series] . append(shuttle)
  return dfs

dfs = collect_raw( raw.source_folder + "csv" )

for s in raw.series:
  dfs[s].to_csv( dest + "/" + s + ".csv",
                 index = False )

