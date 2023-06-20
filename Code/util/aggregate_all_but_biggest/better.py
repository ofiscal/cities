if True:
  from typing import List, Set, Dict
  import numpy as np
  import pandas as pd
  from Code.util.normalize import normalize


if True:
  def add_top_five_column (
      five      : int, # Makes testing easier.
                       # In production, set five = 5.
      money_col : str,
      df0       : pd.DataFrame # a spacetime slice
      ) -> pd.DataFrame:
    """ Expects a spacetime slice. Adds a "top five" column:
        1 for the biggest five budget items, 0 elsewhere. """
    df = df0.sort_values ( money_col,
                           ascending = True )
    df_low  = df.iloc [:-five] . copy ()
    df_high = df.iloc [-five:] . copy ()
    df_low  ["top five"] = 0
    df_high ["top five"] = 1
    return pd.concat ( [df_low, df_high],
                       axis = "rows" )

  if True: # test it
    assert (
      add_top_five_column (
        2, "money",
        pd.DataFrame ( { "money" : [1,11,2,22,3] } ) ) .
      reset_index ( drop=True ) .
      equals ( pd.DataFrame (
        { "money"    : [1,2,3,11,22],
          "top five" : [0,0,0, 1, 1] } ) ) )

if True:
  def add_top_n_column (
      categ_col : str,
      df0 : pd.DataFrame # space slice with "top five" column
      ) -> pd.DataFrame:
    """Expects a space slice with a "top five" column.
Creates a "top n" column, which is 1 for every item category
that is in the top five items for some year. """
    df = df0 . copy ()
    top_rows = df [ df["top five"] == 1 ]
    top_items = set ( top_rows [categ_col]
                      . unique () )
    df ["top n"] = ( df [categ_col] .
                     apply ( lambda cell:
                             int ( cell in top_items ) ) )
    return df

  if True: # Test it
    td = pd.DataFrame ( { "city"     : [1,1,1, 2,2,2],
                          "categ"    : [1,2,3, 1,2,3],
                          "top five" : [0,0,1, 0,1,0] } )
    top_n = pd.DataFrame ( { "top n" : [0,1,1, 0,1,1] } )
      # In city 1, item categ 3 is top-five.
      # In city 2, item categ 2 is.
      # Therefore any row with item categ 2 or 3 is top-n.
    assert ( add_top_n_column ("categ", td) .
             equals( pd.concat ( [td, top_n],
                                 axis = 'columns' ) ) )
    del (td)

if True:
  def sum_all_but_top_n_in_groups (
      group_cols : List [str],
      categ_col : str,
      df0 : pd.DataFrame
      ) -> pd.DataFrame:
    """ In each group, aggregates rows not marked "top n"
        into a single row called "other".
    PITFALL: Changes order of rows.
    PITFALL: Name is very similar to that of a function that uses it.
      That using function is intended to be outward-facing.
      This one would be private, if Python allowed that. """
    df_low  = df0 [ df0 ["top n"] == 0 ] . copy ()
    df_high = df0 [ df0 ["top n"] == 1 ] . copy ()
    others = ( df_low .
               groupby ( group_cols ) .
               sum ( numeric_only = True ) .
               reset_index () )
    others [categ_col] = "Otros"
    return (
      pd.concat (
        [ df_high, others],
        sort = True, # because, Python claims, columns do not align.
                     # TODO ? Why?
        axis = "rows" ) .
      sort_values (
        group_cols +
        [ "top n", # ensure that Others are not in the middle.
          categ_col ] ) )
  if True: # Test it
    td0 = pd.DataFrame ( { "g"     : [1,1,1,1, 2,2,2,2],
                           "categ" : ["a","b","c","d",
                                      "c","d","e","f",],
                           "top n" : [0,0,1,1, 1,1,0,0],
                           "v"     : [1,2,3,4, 1,2,3,4] } )
    td1 = pd.DataFrame ( { "g"     : [1,  1,1, 2,2,  2],
                           "categ" : ["Otros", "c","d",
                                      "c","d", "Otros"],
                          "top n" : [0,  1,1, 1,1,  0],
                          "v"     : [3,  3,4, 1,2,  7] } )
    assert (
      normalize (
        sum_all_but_top_n_in_groups (
          ["g"], "categ", td0 ) )
      . equals ( normalize ( td1 ) ) )
    del (td0,td1)

if True:
  def go ( five       : int, # Makes testing easier.
                             # In production, set five = 5.
           space_cols : List[str],
           time_col   : str,
           categ_col  : str,
           money_col  : str,
           df         : pd.DataFrame
          ) -> pd.DataFrame:
    """
1: In each sapcetime     slice, runs add_top_five_column().
2: In each space (only!) slice, runs add_top_n_column().
3: In each spacetime     slice,
    gruops small rows into an "otros" row,
    uisng sum_all_but_top_n_in_groups()."""
    df1 = ( df . copy () .
            groupby ( space_cols + [time_col] )
            . apply ( lambda df:
                      add_top_five_column ( five, money_col, df ) )
            . reset_index( drop=True ) )
    df2 = ( df1 . groupby ( space_cols,
                            group_keys = False )
            . apply ( lambda df:
                      add_top_n_column ( categ_col, df ) ) .
            reset_index ( drop = True ) )
    df3 = ( df2 . groupby ( space_cols + [time_col] )
            . apply ( lambda df:
                      sum_all_but_top_n_in_groups (
                        space_cols + [time_col],
                        categ_col,
                        df ) ) .
            reset_index ( drop = True ) )
    return df3 . drop ( columns = ["top five","top n"] )
  if True: # test it
    XX = "Otros"
    tx = pd.DataFrame(
      { "where" : [1,1,1,1,1, 1,1,1,1,1, 2,2,2,2,2, 2,2,2,2,2],
        "when"  : [1,1,1,1,1, 2,2,2,2,2, 1,1,1,1,1, 2,2,2,2,2],
        "categ" : [0,1,2,3,4, 0,1,2,3,4, 0,1,2,3,4, 0,1,2,3,4],
        "cash"  : [0,1,2,3,4, 0,1,4,3,2, 5,4,3,2,1, 5,3,4,2,1] } )
    ty = go( 2, ["where"],"when","categ","cash",tx )
    tz = pd.DataFrame(
      { "where" : [1,   1,1,1, 1,   1,1,1, 2,2,2,  2,  2,2,2,  2],
        "when"  : [1,   1,1,1, 2,   2,2,2, 1,1,1,  1,  2,2,2,  2],
        "categ" : [XX,  2,3,4, XX,  2,3,4, 0,1,2,  XX, 0,1,2,  XX],
        "cash"  : [1,   2,3,4, 1,   4,3,2, 5,4,3,  3,  5,3,4,  3] } )
    assert ( normalize ( ty ) .
             equals ( normalize ( tz ) ) )
