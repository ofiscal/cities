# Call this on a subsample size s (not 1, that would be dumb)
# to make sure that recip-s is a "complete" subset of
# recip-1, the full dataset:
# that is, that for every (dept, muni) pair in recip-s,
# the set of rows at those coordinates in recip-1 is equal to
# the set of rows at those coordinates in recip-s.

if True:
  import os
  import pandas as pd
  import numpy as np
  import Code.common as c
  import Code.metadata.four_series as s4
  from Code.util.normalize import normalize

def geo_slice( dept : str,
               muni : str,
               df : pd.DataFrame
             ) -> pd.DataFrame:
  return df[ (df["dept"] == dept) &
             (df["muni"] == muni) ]

def test_geo_slice( dept : str,
                    muni : str,
                    df0 : pd.DataFrame,
                    df1 : pd.DataFrame
                  ) -> bool:
  return ( normalize(
             geo_slice( dept, muni, df0 ) ) .
           equals(
             normalize(
               geo_slice( dept, muni, df1 ) ) ) )

def compare( small : pd.DataFrame,
             large : pd.DataFrame
           ):
  places = ( small[["dept","muni"]] .
             groupby( ["dept","muni"] ) .
             apply( lambda df: df.iloc[0] ) .
             reset_index( drop=True ) )
  ( places .
    apply( lambda place:
           test_geo_slice( place["dept"], place["muni"],
                           small, large ),
           axis = "columns" ) )

small_folder = "output/budget_7_verbose/recip-" + str(c.subsample)
large_folder = "output/budget_7_verbose/recip-1"
for filename in list( map( lambda s: s.name, s4.series ) ):
  print(filename)
  small = pd.read_csv( small_folder + "/" + filename + ".csv" )
  large = pd.read_csv( large_folder + "/" + filename + ".csv" )
  compare( small, large )

