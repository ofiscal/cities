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

if True:
  def add_top_n_column(
      df0 : pd.DataFrame
      ) -> pd.DataFrame:
    """ Expects a space slice with a "top five" column.
    Creates a "top n" column, which is 1 for every item category
    that is in the top five items for some year. """
    df = df0.copy()
    top_rows = df[ df["top five"] == 1 ]
    top_items = set( top_rows["item categ"].unique() )
    df["top n"] = ( df["item categ"] .
                    apply( lambda cell: int( cell in top_items ) ) )
    return df
  if True: # Test it
    td = pd.DataFrame( { "city"       : [1,1,1, 2,2,2],
                         "item categ" : [1,2,3, 1,2,3],
                         "top five"   : [0,0,1, 0,1,0] } )
    top_n = pd.DataFrame( { "top n"   : [0,1,1, 0,1,1] } )
      # In city 1, item categ 3 is top-five.
      # In city 2, item categ 2 is.
      # Therefore any row with item categ 2 or 3 is top-n.
    assert ( add_top_n_column(td) .
             equals( pd.concat( [td, top_n],
                                axis = 'columns' ) ) )

