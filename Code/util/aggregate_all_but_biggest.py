if True:
  from typing import List, Set, Dict
  import numpy as np
  import pandas as pd

test_data = ( # for safety, these names are similar but intentionally not
              # identical to the ones used in production
  pd.DataFrame( {
    "yr"    : [1,1,1,1,  2,2,2,2],
    "yr+1"  : [2,2,2,2,  3,3,3,3], # ala the (dept,dept code) redundancy
    "categ" : [0,1,2,3,  0,1,2,3],
    "money" : [0,1,2,3,  10,11,12,13] } ) .
  sort_values( ["yr","money"] ) )

def last_n_in_groups(
    n : int,
    group_vars : List[str],
    df : pd.DataFrame
    ) -> pd.DataFrame:
  """ Groups the data by group_vars.
  Keep only the top n rows in each group.
   """
  return (
    df.copy() .
    groupby( group_vars ) .
    apply( lambda df: df . tail(n) ) .
    reset_index( drop = True ) )

if True: # test it
  assert (
    last_n_in_groups( 2, ["yr"], test_data ) .
    equals(
      pd.DataFrame( {"yr"    : [1, 1,  2,  2],
                     "yr+1"  : [2, 2,  3,  3],
                     "categ" : [2, 3,  2,  3],
                     "money" : [2, 3, 12, 13] } ) ) )

def sum_of_all_but_last_n_rows_in_groups(
    n : int,
    group_vars : List[str],
    df0 : pd.DataFrame
    ) -> pd.DataFrame:
  """ This drops the last (not the greatest) `n` rows, and sums the rest.
  PITFALL: Has a very similar name to a function that uses it.
    That using function is intended to face out of this module;
    this one would be private, if Python allowed that.
  """
  return (
    df0.copy() .
    groupby( group_vars ) .
    apply( lambda df: df . iloc[:-n] ) .
    reset_index( drop = True ) .
    groupby( group_vars ) .
    agg( sum ) .
    reset_index() )

if True: # test it
  assert (
    sum_of_all_but_last_n_rows_in_groups(
      n = 2,
      group_vars = ["yr","yr+1"],
      df0 = test_data ) .
    drop( columns = "categ" ) . # meaningless when summed
    equals( pd.DataFrame( { "yr"    : [1,2],
                            "yr+1"  : [2,3],
                            "money" : [1,21] } ) ) )

def sum_all_but_greatest_n_rows_in_groups(
    n                  : int,
    group_vars         : List[str],
    sort_vars          : List[str],
    meaningless_to_sum : List[str],
    df0                : pd.DataFrame
    ) -> pd.DataFrame:
  """ PITFALL: Has a very similar name to a function it uses.
  This is only function intended to face out of this module;
  the two it uses would be private, if Python allowed that. """
  df = ( df0 . copy() .
         sort_values( group_vars + sort_vars ) )
  indiv = last_n_in_groups( n, group_vars, df )
  grouped = sum_of_all_but_last_n_rows_in_groups(
    n, group_vars, df )
  for c in meaningless_to_sum:
    grouped[c] = "Otros"
  return ( pd.concat( [indiv, grouped],
                      sort = True ) .
           sort_values( group_vars ) )

if True: # test it
  assert (
    sum_all_but_greatest_n_rows_in_groups(
      2, ["yr","yr+1"], ["money"], ["categ"], test_data ) .
    reset_index( drop = True ) .
    equals (
      pd.DataFrame( { "categ"  : [2,3,"Otros",
                                  2,3,"Otros"],
                      "money"  : [2,3,1,
                                12,13,21],
                      "yr"     : [1,1,1,
                                  2,2,2],
                      "yr+1"   : [2,2,2,
                                  3,3,3] } ) ) )
