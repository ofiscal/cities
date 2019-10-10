# This file demosntrates incompleteness of the data.
# There are four kinds of taxes: regalias, and the three from Sisfut.
# For some spacetime values, one or the other is missing.

import pandas as pd

if True: # input data to demonstrate the problem
  df0 = pd.read_csv(
    "output/budget_7_verbose/recip-1/ingresos.csv" )
  pd.set_option('display.min_rows', 100)
  pd.set_option('display.max_rows', 100)
  spacetime = ["dept code","muni code","year","dept","muni"]

if True: # Find the 46 (muni,year) pairs for which not all four are present
         # (and yet for which at least one *is* present;
         # if all 4 are ever absent, that pair won't show up here).
  counts = {}
  df = df0.copy()
  df["rows"] = 1
  df = df.groupby(spacetime).sum().reset_index()
  df[ df["rows"] < 4 ]
  len(df[ df["rows"] < 4 ])

if True: # investigate an example:
  # The last row of the previous result is
  # dept 99, muni  99773, year 2018.
  # It has a "rows" value of 1, meaning (probably) regalias is present
  # and the 3 from sisfut are absent.
  # Let's see if that's true in the raw data:
  orig = pd.read_csv(
    "output/budget_0_collect/ingresos.csv" )
  orig[ (orig["dept code"]==99) &
        (orig["muni code"]==99773) &
        (orig["year"]==2018) ] # Looks like it's missing in the raw data.
  # Now let's see what happened for that same region in the previous year:
  orig[ (orig["dept code"]==99) &
        (orig["muni code"]==99773) &
        (orig["year"]==2017) ] # That data is not missing.

