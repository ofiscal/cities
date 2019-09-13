# For eyeballing whether the deflation step works.
# Data from 2018 should be unchanged;
# data from 2017 should be slightly changed;
# the earliest data should change by around 30%.
# See output/inflation.csv for precise figures.

import os
import pandas as pd

import Code.common as c
import Code.series_metadata as ser


source_5 = "output/budget_5_add_regalias/recip-" + str(c.subsample)
dfs5 = {}
for s in ser.series:
  dfs5[s.name] = pd.read_csv( source_5 + "/" + s.name + ".csv",
                              encoding = "utf-8" )

source_6 = "output/budget_6_deflate/recip-" + str(c.subsample)
dfs6 = {}
for s in ser.series:
  dfs6[s.name] = pd.read_csv( source_6 + "/" + s.name + ".csv",
                              encoding = "utf-8" )

dfms = {} # m for merge
axes = ["muni code","year","item code"]
for s in ser.series:
  keepers = axes + [s.pesos_col]
  dfms[s.name] = (
           dfs5[s.name][keepers] . sort_values(axes) .
    merge( dfs6[s.name][keepers] . sort_values(axes),
           on = ["muni code","year","item code"] ) )
  print( dfms[s.name] )
