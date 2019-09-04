if True:
  from typing import List
  import pandas as pd

test_data = (
  pd.DataFrame( { "year"      : [1,1,1,1,2,2,2,2],
                  "item code" : [0,1,2,3,0,1,2,3],
                  "value"     : [0,1,2,3,
                                 10,11,12,13] } ) .
  sort_values( ["year","value"],
               ascending = False ) )

def first_n_in_groups(
    n : int,
    group_vars : List[str],
    df : pd.DataFrame
    ) -> pd.DataFrame:
  """ Groups the data by group_vars.
  Keep only the top n rows in each group.
   """
  return (
    df .
    groupby( group_vars ) .
    apply( lambda df: df . head(n) ) .
    reset_index( drop = True ) )

if True: # test it
  assert (
    first_n_in_groups( 2, ["year"], test_data ) .
    equals(
      pd.DataFrame( {"year"      : [1,1,2,2],
                     "item code" : [3,2,3,2],
                     "value"     : [3,2,13,12] } ) ) )

def sum_all_but_first_n_rows_in_groups(
    n : int,
    group_vars : List[str],
    df : pd.DataFrame
    ) -> pd.DataFrame:
  return (
    df .
    groupby( "year" ) .
    apply( lambda df: df . iloc[n:] ) .
    reset_index( drop = True ) .
    groupby( group_vars ) .
    agg( sum ) .
    reset_index() )

if True: # test it
  assert (
    sum_all_but_first_n_rows_in_groups( 2,
                                        ["year"],
                                        test_data ) .
    drop( columns = "item code" ) . # meaningless after summation
    equals( pd.DataFrame( { "year" : [1,2],
                            "value" : [1,21] } ) ) )
