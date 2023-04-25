###### PURPOSE:
###### Collect SISFUT data across years.
###### Creates these four files in output/budget_0_collect/,
###### each line of which represents a budget item,
###### i.e. a source of tax revenue or an expenditure:
######   deuda.csv
######   funcionamiento.csv
######   ingresos.csv
######   inversion.csv

###### WHY THIS IS ITS OWN FILE:
###### Rerunning this step takes forever.
###### Isolating it means the Makefile will not rerun it unnecessarily.

if True:
  import numpy as np
  import os
  import pandas as pd
  from   typing import Set
  #
  import Code.common as common
  import Code.metadata.raw_series as raw


if True:
  dest = os.path.join ( common.outdata,
                        "budget_0_collect" )
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
          os.path.join ( source,
                         str(year) + "_" + series + ".csv" ),
          usecols = set.union(
            extra_columns,
            set.difference(
              set( raw.column_subsets_long[series] ),
              raw.omittable_columns_long ) ), # omit the omittable ones
          **kwargs ) .
        rename( columns = dict( raw.column_subsets[series] ) ) )
      shuttle["year"] = year
      dfs[series] = pd.concat( [ dfs[series],
                                 shuttle ] )
  return dfs

dfs = collect_raw ( os.path.join (
  common.indata,
  "sisfut", "csv" ) )

for s in raw.series:
  dfs[s].to_csv( dest + "/" + s + ".csv",
                 index = False )
