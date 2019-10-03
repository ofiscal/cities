if True:
  from typing import Set
  import numpy as np
  import pandas as pd
  #
  import Code.metadata.raw_series as sm


def collect_raw( source : str,
                 extra_columns : Set[str] = set(),
                 **kwargs ):
  """Returns a dictionary of three data frames, one for each of ingresos, inversion and funcionamiento. If using the optional 'nrows' argument, bear in mind that the 3 data sets have about 4 million rows between them."""
  dfs = {}
  for series in sm.series:
    dfs[series] = pd.DataFrame()
    for year in range( 2012, 2018+1 ):
      shuttle = (
        pd.read_csv(
          source + "/" + str(year) + "_" + series + ".csv",
          usecols = set.union(
            extra_columns,
            set.difference(
              set( sm.column_subsets_long[series] ),
              sm.omittable_columns_long ) ), # omit the omittable ones
          **kwargs ) .
        rename( columns = dict( sm.column_subsets[series] ) ) )
      shuttle["year"] = year
      dfs[series] = dfs[series] . append(shuttle)
  return dfs

