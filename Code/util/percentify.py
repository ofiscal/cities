if True:
  from typing import List,Set,Dict
  import pandas as pd


def percentify_columns( cols : List[str],
                        df0 : pd.DataFrame
                      ) -> pd.DataFrame:
  """ Divides each column in `cols` by its total.
  Makes sense to apply to a spacetime cell,
  but not to a dataframe with multiple years or municipalities. """
  # TODO ? Would this be faster and still safe without the copy?
  df = df0.copy()
  sums = df[cols].sum()
  for c in cols: df[c] = df[c] / sums[c]
  return df

if True: # test it
  x = pd.DataFrame( [[1,2,3],
                     [4,6,8]],
                    columns = ["moon","helium","art"] )
  y = percentify_columns(["moon","helium"],x)
  z = pd.DataFrame( [[0.2,0.25,3],
                     [0.8,0.75,8]],
    columns = ["moon","helium","art"] )
  assert y.equals(z)

def percentify_columns_by_groups(
    by : List[str], # group by these
    cols : List[str], # percentify these
    df : pd.DataFrame
    ) -> pd.DataFrame:
  return ( df . groupby( by ) .
           apply( lambda df :
                  percentify_columns( cols, df ) ) )

if True: # test it
  x = pd.DataFrame( {
    "g" : [1,1,2,2],
    "v" : [1,4,1,9] } )
  should_be = pd.DataFrame( {
    "g" : [1,1,2,2],
    "v" : [1/5,4/5,1/10,9/10] } )
  really_is = (
    percentify_columns_by_groups(
      by = ["g"],
      cols = ["v"],
      df = x ) .
    reset_index( drop = True ) )
  assert should_be.equals( really_is )
