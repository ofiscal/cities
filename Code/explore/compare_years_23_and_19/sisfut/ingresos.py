# GOOD NEWS!
# The ingresos data not to have changed in format at all.

from typing import List, Dict, GenericAlias
import os.path as path
import pandas as pd
import numpy as np


#####
##### Define paths
#####

year : GenericAlias = int
in19 = "data/2019/sisfut/csv"
in23 = "data/2023/sisfut/csv"
out19 = "output/2019"


#####
##### In inputs, compare column names and dtypes
#####

# The "view as of" (vao) years 19 and 23.
# This will be a dictionary, the keys of which are 2-digit years,
# and the values of which are pandas data frames.
vao19 : Dict [year, pd.DataFrame] = {}
vao23 : Dict [year, pd.DataFrame] = {}

for y in range(13,22):
  vao23[y] = pd.read_csv (
    path.join ( in23, "20" + str(y) + "_ingresos.csv" ) )
  if y <= 18:
    vao19[y] = pd.read_csv (
      path.join ( in19, "20" + str(y) + "_ingresos.csv" ) )

# As of 2019, each data frame had the same columns amd dtypes.
for df in vao19.values():
  print(df.columns
        .equals(
          vao19[13].columns ) )
  print(df.dtypes
        .equals(
          vao19[13].dtypes ) )

# As of 2023, the same was true.
for df in vao23.values():
  print(df.columns
        .equals(
          vao23[13].columns ) )
  print(df.dtypes
        .equals(
          vao23[13].dtypes ) )

# In fact, the set of column names is equal across the two views!
( vao19[13].columns
  . equals(
    vao23[13].columns ) )

# The dtypes are *not* equal across the two views ...
mismatches = pd.DataFrame()
for c in vao23[13].columns:
  if (vao19[13][c].dtype) != (vao23[13][c].dtype):
    mismatches = pd.concat (
      [ mismatches,
        pd.Series ( { "column" : c,
                      "2013 type" : vao19[13][c].dtype,
                      "2016 type" : vao23[13][c].dtype } ) ],
      axis = "columns" )
mismatches = mismatches.transpose()
mismatches

# ... but that's only because the view as of 2019 has a format problem --
# numbers appear as strings because they include commas.
( vao19[13]
  [list(mismatches["column"])] )
