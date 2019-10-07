if True:
  from typing import List, Set, Dict
  import numpy as np
  import pandas as pd
  from Code.util.normalize import normalize

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
    del(td)

if True:
  def sum_all_but_top_n_in_groups(
      group_cols : List[str],
      categ_col : str,
      df0 : pd.DataFrame
      ) -> pd.DataFrame:
    """ In each group, aggregates rows not marked "top n"
        into a single row called "other".
    PITFALL: Changes order of rows.
    PITFALL: Name is very similar to that of a function that uses it.
      That using function is intended to be outward-facing.
      This one would be private, if Python allowed that. """
    df_low  = df0[ df0["top n"] == 0 ].copy()
    df_high = df0[ df0["top n"] == 1 ].copy()
    others = ( df_low .
               groupby( group_cols ) .
               agg( sum ) .
               reset_index() )
    others[categ_col] = "Otros"
    return (
      pd.concat( [ df_high, others],
                 axis = "rows" ) .
      sort_values(
        group_cols +
        [ "top n", # ensure that Others are not in the middle.
          categ_col] ) )
  if True: # Test it
    td0 = pd.DataFrame( { "g"     : [1,1,1,1, 2,2,2,2],
                          "categ" : ["a","b","c","d",
                                     "c","d","e","f",],
                          "top n" : [0,0,1,1, 1,1,0,0],
                          "v"     : [1,2,3,4, 1,2,3,4] } )
    td1 = pd.DataFrame( { "g"     : [1,  1,1, 2,2,  2],
                          "categ" : ["Otros", "c","d",
                                     "c","d", "Otros"],
                          "top n" : [0,  1,1, 1,1,  0],
                          "v"     : [3,  3,4, 1,2,  7] } )
    assert (
      normalize(
        sum_all_but_top_n_in_groups(
          ["g"], "categ", td0 ) ) .
      equals( normalize( td1 ) ) )
    del(td0,td1)

assert False == "RESUME HERE"
def go( space_cols : List[str],
        time_col   :      str,
        money_col  :      str,
        categ_col  :      str,
        df         : pd.DataFrame
      ) -> pd.DataFrame:
  """ 
  1 - In each sapcetime     slice, runs add_top_five_column().
  2 - In each space (only!) slice, runs add_top_n_column().
  3 - In each spacetime     slice, aggregate small rows into an "otros" row.
  5 - In each spacetime     slice, appends 3 to the end of 4. """
  df1 = ( df0 . groupby( space_cols + [time_col] ) .
          apply( lambda df:
                 add_top_five_column( 5, money_var, df ) ) .
          reset_index() )
  df2 = ( df1 . groupby( space_cols ) .
          apply( add_top_n_column ) .
          reset_index() )
  df3 = ( df2 . groupby( space_cols + [time_col] ) .
          apply( 
