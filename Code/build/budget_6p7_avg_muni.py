# PURPOSE:
# In the -pct files, compute an "average municipality"
# for each district.

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  #
  import Code.common as c
  from Code.util.percentify import percentify_columns
  import Code.metadata.two_series as s2
  import Code.metadata.four_series as s4

if True: # folders
  source  = "output/budget_6p5_cull_and_percentify/recip-" + str(c.subsample)
  dest = "output/budget_6p7_avg_muni/recip-"               + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

spacetime = ["dept code","muni code","year"]

if True: # input data
  dfs = {}
  for s in s4.series:
    dfs[s.name] = pd.read_csv(
      source + "/" + s.name + ".csv" )

if True: # define how to compute the average muni in a dept
  def prepend_avg_muni( money_cols : [str],
                        df0 : pd.DataFrame
                      ) -> pd.DataFrame:
    """ Input:  All munis in a given department-year.
        Output: The same, plus a new "average" muni. """
    df = ( df0.copy()
           [df0["muni code"] != -1] )
             # omit department-level data; use only munis
    avg = df.iloc[0]
    avg[money_cols] = df[money_cols].mean()
    avg["muni code"] = -2 # TODO ? Ugly.
    return pd.concat( [ pd.DataFrame([avg]),
                        df0],
                      axis="rows" )
  if True: # test it
    x = pd.DataFrame( [ [13, -1, 1, 2, 1],
                        [13,  1, 2, 2, 2],
                        [13,  2, 3, 6, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","moolah"] )
    y = pd.DataFrame( [ [13, -2, 2.5, 4, 2],
                        [13, -1, 1,   2, 1],
                        [13,  1, 2,   2, 2],
                        [13,  2, 3,   6, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","moolah"] )
    assert ( prepend_avg_muni( ["money","cash"], x) .
             reset_index(drop=True) .
             equals( y.astype('float') ) )

if True:
    money_cols = ["money","cash"]
    xx = ( x.copy()
           [x["muni code"] != -1] )
             # omit department-level data; use only munis
    avg = xx.iloc[0]
    avg[money_cols] = xx[money_cols].mean()
    avg["muni code"] = -2 # TODO ? Ugly.

1
# for s in s2.series:
#   df = dfs[s.name + "-pct"]
#   dfs[s.name + "-pct"] = df

assert False == "Test here."

for s in s4.series:
  dfs[s.name].to_csv( dest + "/" + s.name + ".csv" )

