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

# The view as of (vao) year _.
# This will be a dictionary, the keys of which are 2-digit years,
# and the values of which are pandas data frames.
vao19 : Dict [year, pd.DataFrame] = {}
vao23 : Dict [year, pd.DataFrame] = {}

vao19[13] = pd.read_csv (
  path.join ( in19, "2013_deuda.csv" ) )
vao23[13] = pd.read_csv (
  path.join ( in23, "2013_deuda.csv" ) )


#####
##### Look
#####

pd.options.display.min_rows = 100

vao19[13].dtypes
vao23[13].dtypes

vao19[13].describe().transpose()
vao23[13].describe().transpose()
