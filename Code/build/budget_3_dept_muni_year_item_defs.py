from typing import List
import numpy as np
import pandas as pd


def group_is_redundant(
    redundant_field : str,
    group_fields : List[str],
    df : pd.DataFrame ) -> bool:
  """ Assumes df is a data frame grouped by some columns, one of which is redundant_field. Verifies that redundant_field is redundant. """
  df2 = df.copy()
  df2["one"] = 1
  df2 = ( df2 .
         groupby( by = [ f for f in group_fields
                         if f != redundant_field] ) .
         agg( sum ) )
  return df2["one"].max() == 1

if True: # Tests
  # That it works, and that it leaves its argument unchanged.
  if True: # where it should return True
    x = ( 
      pd.DataFrame(
        [ [1,1,1],
          [1,1,2],
          [2,2,3],
          [2,2,4] ],
        columns = ["a","b","c"] ) .
      groupby( by = ["a","b"] ) .
      agg( sum ) )
    y = x.copy()
    assert group_is_redundant( "b",
                               ["a","b"],
                               x )
    assert x.equals(y)
  if True: # where it should return False  
    x = ( 
      pd.DataFrame(
        [ [1,1,1],
          [1,7,2], # Due to the 7, "b" is not redundant.
          [2,2,3],
          [2,2,4] ],
        columns = ["a","b","c"] ) .
      groupby( by = ["a","b"] ) .
      agg( sum ) )
    y = x.copy()
    assert not group_is_redundant( "b",
                                   ["a","b"],
                                   x )
    assert x.equals(y)
