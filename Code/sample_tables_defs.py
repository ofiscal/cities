if True:
  from typing import List, Set, Dict
  import numpy as np
  import pandas as pd

test_data = (
  pd.DataFrame( {
    "year"      : [1,1,1,1,2,2,2,2],
    "year+1"    : [2,2,2,2,3,3,3,3], # ala the (dept,dept code) redundancy
    "item code" : [0,1,2,3,0,1,2,3],
    "value"     : [0,1,2,3,
                   10,11,12,13] } ) .
  sort_values( ["year","value"] ) )

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
    last_n_in_groups( 2, ["year"], test_data ) .
    equals(
      pd.DataFrame( {"year"      : [1,1,2,2],
                     "year+1"    : [2,2,3,3],
                     "item code" : [2,3,2,3],
                     "value"     : [2,3,12,13] } ) ) )

def sum_of_all_but_last_n_rows_in_groups(
    n : int,
    group_vars : List[str],
    df0 : pd.DataFrame
    ) -> pd.DataFrame:
  """ PITFALL: Has a very similar name to a function that uses it.
  That using function is intended to face out of this module;
  this one would be private, if Python allowed that. """
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
      group_vars =["year","year+1"],
      df0 = test_data ) .
    drop( columns = "item code" ) .
    equals( pd.DataFrame( { "year"   : [1,2],
                            "year+1" : [2,3],
                            "value"  : [1,21] } ) ) )

def sum_all_but_greatest_n_rows_in_groups(
    n : int,
    group_vars : List[str],
    sort_vars : List[str],
    meaningless_to_sum : List[str],
    df0 : pd.DataFrame
    ) -> pd.DataFrame:
  """ PITFALL: Has a very similar name to a function it uses.
  This is only function intended to face out of this module;
  the two it uses would be private, if Python allowed that. """
  df = ( df0 . copy() .
         sort_values( group_vars + sort_vars ) )
  indiv = last_n_in_groups( n, group_vars, df )
  grouped = sum_of_all_but_last_n_rows_in_groups(
    n, group_vars, df )
  grouped = grouped.drop(
    columns = set.intersection( # TODO : why do I need this hack?
      # Dropping meaningless_to_sum seems like it should be enough;
      # I shouldn't have to first take the intersection below.
      # In fact, that works for the test data (in this file),
      # but somehow on the real data (e.g. tables.py) it doesn't.
      set(meaningless_to_sum),
      set(grouped.columns) ) )
  return ( pd.concat( [indiv, grouped],
                      sort = True ) .
           sort_values( group_vars ) )

if True: # test it
  assert (
    sum_all_but_greatest_n_rows_in_groups(
      2, ["year","year+1"], ["value"], ["item code"], test_data ) .
    reset_index( drop = True ) .
    equals (
      pd.DataFrame( { "item code" : [2,3,np.nan,
                                     2,3,np.nan],
                      "value"     : [2,3,1,
                                    12,13,21],
                      "year"      : [1,1,1,
                                     2,2,2],
                      "year+1"    : [2,2,2,
                                     3,3,3] } ) ) )
