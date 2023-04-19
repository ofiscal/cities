if True:
  from typing import List
  import pandas as pd


# If some reordering of rows and columns can render x == y,
# then normalize(x) == normalize(y).
def normalize( df : pd.DataFrame
             ) -> pd.DataFrame:
  cs = list(sorted(df.columns))
  return ( df .
           sort_values( cs ) .
           reset_index( drop = True )
           [cs] )
