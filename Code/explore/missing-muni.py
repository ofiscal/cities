# For testing whether a data frame contains department info --
# i.e. whether some rows are missing muni code,
# and if so, what they're like.

if True:
  import pandas as pd
  import numpy as np
  import Code.build.sisfut_metadata as sis
  import Code.series_metadata as ser


if True: # setup
  source = "output/budget_6_deflate/recip-10"
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

if True: # print stuff
  for s in file_indices:
    print( s )
    df = dfs[s]
    print( len(df) )
    # put another print statement here
    print( df.describe().transpose()[["count","min","mean","max"]] )

if False: # some print statements
    print( df.iloc[0] )
    print( df.describe().transpose()[["count","min","mean","max"]] )
    print( len( df[~null_muni]["dept code"].unique() ) )
    print( len( df[ null_muni]["dept code"].unique() ) )
    print( df )
