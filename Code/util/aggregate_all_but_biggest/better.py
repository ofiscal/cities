if True:
  from typing import List, Set, Dict
  import numpy as np
  import pandas as pd

if True:
  def add_top_five_column(
      five : int, # when testing it might not be five
      money_col : str,
      df0 : pd.DataFrame # a spacetime slice
      ) -> pd.DataFrame:
    """ Expects a spacetime slice. Adds a "top five" column:
        1 for the biggest five budget items, 0 elsewhere. """
    df = df0.sort_values ( money_col,
                           ascending = True )
    df_low  = df.iloc[:-five].copy()
    df_high = df.iloc[-five:].copy()
    df_low["top five"] = 0
    df_high["top five"] = 1
    return pd.concat( [df_low,df_high],
                      axis = "rows" )
  if True: # test it
    assert (
      add_top_five_column(
        2, "money",
        pd.DataFrame( { "money" : [1,11,2,22,3] } ) ) .
      reset_index( drop=True ) .
      equals( pd.DataFrame(
        { "money" : [1,2,3,11,22],
          "top five" : [0,0,0,1,1] } ) ) )

