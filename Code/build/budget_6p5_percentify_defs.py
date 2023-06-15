import pandas as pd


def no_dups_index ( col : str,
                    df : pd.DataFrame
                   ) -> pd.Series:
  """
  Returns a subset of the index of `df` along which no values in `col` are duplicated.
  PITFALL: Needs an explicit, non-repeating) "index" column."""
  return ( df . groupby ( col )
           . agg ("first")
           . reset_index ( drop=True )
           ["index"] )
assert (
  no_dups_index (
    "value",
    pd.DataFrame ( {
      "index" : [0,1,2,3,4,5,6], # unused; just illustrative
      "value" : [1,1,2,3,4,4,4] } ) )
  . equals (
    pd.Series ( [0,2,3,4] ) ) )

def order_of_both_values_the_same (
    unique_col : str,
    other_col : str,
    df : pd.DataFrame
) -> bool:
  """
  Determines whether,
  after reducing `df` to a subset upon which `unique_col` is unique,
  sorting by `unique_col` or `other_col` returns the same result."""
  i = no_dups_index ( col = unique_col, df = df )
  return ( df.loc[i] . sort_values ( unique_col )
           . equals (
             df.loc[i] . sort_values ( other_col ) ) )
if True: # test it
  assert order_of_both_values_the_same (
    "a", "b",
    pd.DataFrame ( {
      # Notice that slight deviations from the truth in "b"
      # have no effect -- in this case, because
      # 0.21 is, like 0.2, still between 0.1 and 0.3.
      "a"     : [  3,  1,  2,   2,  2],
      "b"     : [0.3,0.1,0.2,0.21,0.2],
      "index" : [  0,  1,   2,  3,  4]
    } ) )
  assert not order_of_both_values_the_same (
    "a", "b",
    pd.DataFrame ( { "a"     : [  3,  1,  2,   2,  2],
                     "b"     : [0.1,0.1,0.2,0.21,0.3],
                     "index" : [  0,  1,   2,  3,  4]
                    } ) )
