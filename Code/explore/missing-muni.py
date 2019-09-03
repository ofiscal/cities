# For testing whether a data frame contains department info --
# i.e. whether some rows are missing muni code,
# and if so, what they're like.

import pandas as pd
import numpy as np
import Code.build.sisfut_metadata as sis
import Code.series_metadata as ser


###### before joining func and inv into gasto, use sis.series

if True:
  source = "output/budget_1"
  dfs = {}
  for s in sis.series:
    dfs[s] = (
      pd.read_csv( source + "/" + s + ".csv",
                   encoding = "utf-16" ) )
if True:
  for s in sis.series:
    df = dfs[s]
    null_muni = pd.isnull( df["muni code"] )
    len( df[~null_muni]["dept code"].unique() )
    len( df[ null_muni]["dept code"].unique() )


###### after joining func and inv into gastos, use ser.series

if True:
  source = "output/budget_2_subsample/recip-10"
  dfs = {}
  for s in ser.series:
    dfs[s.name] = (
      pd.read_csv( source + "/" + s.name + ".csv",
                   encoding = "utf-16" ) )
if True:
  for s in ser.series:
    df = dfs[s.name]
    null_muni = pd.isnull( df["muni code"] )
    len( df[~null_muni]["dept code"].unique() )
    len( df[ null_muni]["dept code"].unique() )
