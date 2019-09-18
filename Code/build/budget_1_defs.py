if True:
  from typing import Set
  import numpy as np
  import pandas as pd
  #
  import Code.metadata.terms as t
  import Code.metadata.four_series as sm


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

def un_latin_decimal_deuda_columns( df : pd.DataFrame ) -> pd.DataFrame:
  peso_columns = list( map( lambda s: s[1],
                            sm.columns_peso[t.deuda] ) )
  for c in peso_columns:
    df[c] = ( df[c] .
              astype( str ) .
              str.replace( ",", "." ) .
              astype( float ) )
  return df

