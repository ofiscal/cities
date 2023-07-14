import pandas as pd


def my_describe ( df : pd.DataFrame ) -> pd.DataFrame:
  return ( df . describe() . transpose ()
           [ ['count', 'mean', 'std', 'min', '50%', 'max'] ] )
