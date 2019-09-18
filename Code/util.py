if True:
  from typing import List, Set, Dict
  import numpy as np
  import pandas as pd

def un_latin_decimal_columns(
    column_names : List[str],
    df : pd.DataFrame
    ) -> pd.DataFrame:
  for c in column_names:
    df[c] = ( df[c] .
              astype( str ) .
              str.replace( ",", "." ) .
              astype( float ) )
  return df

def to_front( front_columns, df ):
  """ Move some columns to the front of a data frame. """
  rear_columns = [ i for i in df.columns
                   if i not in set( front_columns ) ]
  return df[ front_columns + rear_columns ]
if True: # test it
  x = pd.DataFrame( [], columns = ["a","b","c"] )
  assert to_front( ["b","c"], x ).equals(
    pd.DataFrame( [], columns = ["b","c","a"] ) )

def myDescribe( df : pd.DataFrame ) -> pd.DataFrame:
  if True: # define percentiles to report
    low_percentiles = [.01, .02, .05, .1, .2, .5]
    percentiles_reported = (
      pd.Series( low_percentiles +
                 [ 1-i for i in low_percentiles ] ) .
      sort_values() .
      unique() )
    del( low_percentiles )

  numericTypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
  stats = ( df .
            describe( include="all",
                      percentiles = percentiles_reported ) .
            transpose() )

  if True: # count missing as fraction
    stats["missing"] = 1 - stats["count"] / len(df)
    stats = stats.drop( columns = ["count"] )

  if True: # compute the fraction (of numeric columns) below 0
    stats["<0"] = np.nan # if not numeric, the fraction below 0 is silly
    ( stats .
      loc [ df.select_dtypes(include=numericTypes).columns,
            "<0" ]
    ) = ( df[ df.select_dtypes(include=numericTypes).columns ] .
          apply( lambda col:
                 len( col[ col < 0 ] ) ) )

  return stats

