import pandas as pd


def to_front( front_columns, df ):
  """ Move some columns to the front of a data frame. """
  fcs = set( front_columns )
  rear_columns = [i for i in df.columns if i not in fcs]
  return df[ front_columns + rear_columns ]

x = pd.DataFrame( [], columns = ["a","b","c"] )
assert to_front( ["b","c"], x ).equals(
  pd.DataFrame( [], columns = ["b","c","a"] ) )
