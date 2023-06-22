import pandas as pd
from   typing import Callable, List


def compute_stat_of_year_per_space_slice (
    space_cols : List [ str ], # Only to ease testing.
                               # In production, should be
                               # ["dept code", "muni code"].
    stat      : str, # The name of a Callable [ [num], num]],
                     # i.e. `min` or `max`.
    df        : pd.DataFrame
) ->            pd.DataFrame:
  return df . merge (
    ( df . groupby ( space_cols )
      . agg ( {"year" : stat} )
      . rename ( columns = { "year" : "year-" + stat } )
      . reset_index () ),
    on = space_cols )
if True: # test it
  assert (
    compute_stat_of_year_per_space_slice (
      space_cols = ["where"],
      stat = "min",
      df = pd.DataFrame ( { "where" : [1,1,1, 2,2],
                            "year"  : [0,1,2, 5,6] } ) )
    . equals (
      pd.DataFrame ( { "where"    : [1,1,1, 2,2],
                       "year"     : [0,1,2, 5,6],
                       "year-min" : [0,0,0, 5,5] } ) ) )
