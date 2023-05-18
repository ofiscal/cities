# GOOD NEWS!
# The ingresos data not to have changed in format at all.

from typing import List, Dict, GenericAlias
import os.path as path
import pandas as pd
import numpy as np


#####
##### Define paths
#####

Year      : GenericAlias = int
View      : GenericAlias = Dict [Year, pd.DataFrame]
Two_Views : GenericAlias = ( # TODO : Should this be a dictionary?
  View,  # the view from 2019
  View ) # the view from 2023
in19 = "data/2019/sisfut/csv"
in23 = "data/2023/sisfut/csv"
out19 = "output/2019"

def compare_views_from_2019_and_2023 (
    expense : str
) -> Two_Views:
  (vao19,vao23) = load_views_from_2019_and_2023 ( expense )

  for (view, label) in [ (vao19,"19"),
                         (vao23,"23") ]:
    print ( "compare_column_names_and_dtypes_within_view_across_years("
            + label + "):" )
    compare_column_names_and_dtypes_within_view_across_years ( view )

  print("compare_column_names_across_views")
  compare_column_names_across_views ( vao19, vao23 )

  print("demonstrate_dtypes_not_equal_across_views")
  bad_cols = demonstrate_dtypes_not_equal_across_views ( vao19, vao23 )

  print("demonstrate_mismatches_are_due_to_commas_in_numbers_in_one_view")
  demonstrate_mismatches_are_due_to_commas_in_numbers_in_one_view (
    vao19, bad_cols )

  return (vao19,vao23)

def load_views_from_2019_and_2023 ( expense : str ) -> Two_Views:
  # The "view as of" (vao) years 19 and 23.
  # Each view is a dictionary, the keys of which are 2-digit years,
  # and the values of which are pandas data frames.
  vao19 : Dict [Year, pd.DataFrame] = {}
  vao23 : Dict [Year, pd.DataFrame] = {}
  for y in range(13,22):
    vao23[y] = pd.read_csv (
        path.join ( in23, "20" + str(y) + "_" + expense + ".csv" ) )
    if y <= 18:
      vao19[y] = pd.read_csv (
        path.join ( in19, "20" + str(y) + "_" + expense + ".csv" ) )
  return (vao19, vao23)

def compare_column_names_and_dtypes_within_view_across_years (
    v : View ):
  for df in v.values():
    print(df.columns
          .equals(
            v[13].columns ) )
    print(df.dtypes
          .equals(
            v[13].dtypes ) )

def compare_column_names_across_views ( v : View,
                                        w : View ):
  print ( v[13].columns
          . equals(
            w[13].columns ) )

def demonstrate_dtypes_not_equal_across_views (
    v : View,
    w : View
) -> List[str]: # The names of the columns whose types don't match
  mismatches = pd.DataFrame()
  for c in w[13].columns:
    if (v[13][c].dtype) != (w[13][c].dtype):
      mismatches = pd.concat (
        [ mismatches,
          pd.Series ( { "column" : c,
                        "2013 type" : v[13][c].dtype,
                        "2016 type" : w[13][c].dtype } ) ],
        axis = "columns" )
  mismatches = mismatches.transpose()
  print(mismatches)
  return list(mismatches["column"])

def demonstrate_mismatches_are_due_to_commas_in_numbers_in_one_view (
    v : View,
    cols : List[str] # The columns with formatting errors
):
  acc = pd.DataFrame()
  for cname in cols:
    col = v [13] [cname] . astype(str) . dropna()
    acc = pd.concat (
      [ acc,
        ( pd.DataFrame (
          { cname : col [ col . str.match( ".*,.*" ) ] } )
          . reset_index() ) ],
      axis = 1 )
  print(acc)

(vao19,vao23) = compare_views_from_2019_and_2023 ("ingresos")
(vao19,vao23) = compare_views_from_2019_and_2023 ("funcionamiento")
(vao19,vao23) = compare_views_from_2019_and_2023 ("inversion")
