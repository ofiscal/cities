from typing import List, Dict, GenericAlias
import os.path as path
import pandas as pd
import numpy as np


#####
##### Load
#####

year : GenericAlias = int
in19 = "data/2019/sisfut/csv"
in23 = "data/2023/sisfut/csv"

# The "view as of" (vao) years 19 and 23.
# This will be a dictionary, the keys of which are 2-digit years,
# and the values of which are pandas data frames.
vao19 : Dict [year, pd.DataFrame] = {}
vao23 : Dict [year, pd.DataFrame] = {}

for y in range(13,22):
  vao23[y] = pd.read_csv (
    path.join ( in23, "20" + str(y) + "_deuda.csv" ) )
  if y <= 18:
    vao19[y] = pd.read_csv (
      path.join ( in19, "20" + str(y) + "_deuda.csv" ) )


#####
##### Look
#####

# As of 2019, each data frame had the same columns amd dtypes
for df in vao19.values():
  print(df.columns
        .equals(
          vao19[13].columns ) )
  print(df.dtypes
        .equals(
          vao19[13].dtypes ) )

# As of 2023, each data frame had the same columns
for df in vao23.values():
  print(df.columns
        .equals(
          vao23[13].columns ) )

# and they *mostly* had the same dtypes:
pd.options.display.min_rows = 500
for df in vao23.values():
  print(df.dtypes
        .equals(
          vao23[13].dtypes ) )

# The exception is at year 16, and it's no big deal --
# it just uses ints where the others use floats.
mismatches = pd.DataFrame()
for c in vao23[13].columns:
  if (vao23[13][c].dtype) != (vao23[16][c].dtype):
    mismatches = pd.concat (
      [ mismatches,
        pd.Series ( { "column" : c,
                      "2013 type" : vao23[13][c].dtype,
                      "2016 type" : vao23[16][c].dtype } ) ],
      axis = "columns" )
mismatches.transpose()

# The sets of columns aren't the same in the two views
# (i.e. the view from 2019 and the view from 2023).
( vao19[13].columns
  . equals(
    vao23[13].columns )
