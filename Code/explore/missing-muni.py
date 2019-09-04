# For testing whether a data frame contains department info --
# i.e. whether some rows are missing muni code,
# and if so, what they're like.

import pandas as pd
import numpy as np
import Code.build.sisfut_metadata as sis
import Code.series_metadata as ser


if True: # setup
  source = "output/budget_3_dept_muni_year_item/recip-10"
  if source == "output/budget_1":
        file_indices = sis.series
  else: file_indices = list( map( lambda x: x.name,
                                  ser.series ) )

if True: # read
  dfs = {}
  for s in file_indices:
    dfs[s] = (
      pd.read_csv( source + "/" + s + ".csv",
                   encoding = "utf-16" ) )

if True: # check some lengths
  for s in file_indices:
    df = dfs[s]
    null_muni = pd.isnull( df["muni code"] )
    print( s )
    # put another print statement here
    print( df.describe().transpose()[["count","min","mean","max"]] )

if False: # some print statements
    print( df.iloc[0] )
    print( df.describe().transpose()[["count","min","mean","max"]] )
    print( len( df[~null_muni]["dept code"].unique() ) )
    print( len( df[ null_muni]["dept code"].unique() ) )
    print( df )
