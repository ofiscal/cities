from   typing import List, Set, Dict
import pandas as pd


def get_muni_count (
    dept_level_counts : Dict [str, pd.DataFrame],
      # The index of each `DataFrame` in `dept_level_counts` is the dept code.
      # The column names in each are ["munis", "muni-years"]
    muni_counts       : pd.Series,
    filename          : str,
    dept_code         : int
) -> int:
  """A helper function for getting data from `dept_level_counts`."""
  return ( int ( dept_level_counts [filename] .
                 loc [ dept_code, "munis" ] )
           if dept_code in muni_counts . index
           else 1 ) # TODO ? ugly, ought to be Optional.
# (In that case I would return Nothing for depts with only dept-level info.)
#
# PITFALL: This default value is ultimately not important,
# because every dept code is present in `dept_level_counts`
# in the full sample.
# For proof see the test in
#   `Code/build/budget_6p7_avg_muni.py`
# that bears the comment
# "In full sample, every dept is present in both `DataFrame`s in `dept_level_counts`."

def get_muni_year_count (
    dept_level_counts : Dict [str, pd.DataFrame],
      # The index of each `DataFrame` in `dept_level_counts` is the dept code.
      # The column names in each are ["munis", "muni-years"]
    muni_counts       : pd.Series,
    filename          : str,
    dept_code         : int
) -> int:
  """A helper function for getting data from `dept_level_counts`."""
  return ( int ( dept_level_counts [filename] .
                loc [ dept_code, "muni-years" ] )
           if dept_code in muni_counts . index
           else 3 ) # TODO ? ugly, ought to be Optional.
# (In that case I would return Nothing for depts with only dept-level info.)
#
# PITFALL: This default value is ultimately not important,
# because every dept code is present in `dept_level_counts`
# in the full sample.
# For proof see the test in
#   `Code/build/budget_6p7_avg_muni.py`
# that bears the comment
# "In full sample, every dept is present in both `DataFrame`s in `dept_level_counts`."
