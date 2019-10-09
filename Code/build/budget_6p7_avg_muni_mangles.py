# This is like budget_6p7_avg_muni, but doesn't copy the entirety,
# and diverges in a few places toward the end (search for the word "diverge").

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  #
  import Code.common as c
  from Code.util.misc import to_front
  import Code.build.use_keys as uk
  import Code.metadata.four_series as s4

if True: # folders
  source = ( "output/budget_6p5_cull_and_percentify/recip-"
             + str(c.subsample) )
  dest   = ( "output/budget_6p7_avg_muni/recip-"
             + str(c.subsample) )
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input data
  geo = ( uk.depts_and_munis
         [["dept code","muni code","muni count"]] )
  dfs0, dfs1 = {}, {}
  for s in s4.series:
    dfs0[s.name] = pd.read_csv(
      source + "/" + s.name + ".csv" )

if True: # define how to compute the average non-dept muni
         # in some (dept,year,item categ) cell
  def prepend_avg_muni( index_cols : List[str],
                        money_cols : List[str],
                        df0 : pd.DataFrame
                      ) -> pd.DataFrame:
    """
Input: A slice with constant (dept,year,item categ).
Output: The same, plus a new "average" muni.
        Average is only over true munis; depts are omitted.
"""
    df = ( df0.copy()
           [df0["muni code"] != 0] .
          reset_index() )
    if len(df) == 0: return df0
      # Some subsamples have a dept with no munis.
      # In that case, don't add the average muni.
    munis_in_dept = int(
        geo.loc[ ( geo       ["dept code"] ==
                   df.iloc[0]["dept code"] ),
                 "muni count" ] .
        head(1) )
    avg = df.iloc[0] . copy()
    avg["muni code"] = -2 # TODO ? Ugly.
    avg[money_cols] = ( # The missing-rows-aware mean.
        df[money_cols] . sum() / munis_in_dept )
    return (
      pd.concat( [ pd.DataFrame([avg]),
                   df0 ], # df0, not df, to keep dept-level rows
                 axis="rows",
                 sort=True ) . # because unequal column orders
      drop(columns = ["index"] + index_cols ) )
  if True: # test it
    x = pd.DataFrame( [ [99, 0,   1, 2, 1],
                        [99, 1,   1, 65, 2],
                        [99, 2,   5, 15, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","pecan"] )
    y = ( pd.DataFrame( [ [99, -2, 1.5, 20, 2],
      # The previous row (the only new one) has
      # average money=(1+5) / 4  (because dept 99 has 4 munis)
      # average cash=(15+65) / 4 (because dept 99 has 4 munis)
      # and is otherwise just like the first non-dept muni.
                          [99,  0, 1,    2, 1],
                          [99,  1, 1,   65, 2],
                          [99,  2, 5,   15, 3] ],
                        columns = ["dept code", "muni code",
                                   "money","cash","pecan"] ) .
          astype(float) )
    z = ( prepend_avg_muni( ["dept code"], ["money","cash"], x) .
          reset_index(drop=True) )
    for cn in ["muni code","cash","money","pecan"]:
      assert y[cn].equals(z[cn])

for s in s4.series_pct: # add average muni to the -pct data sets
  dfs1[s.name[:-4]] = dfs0[s.name[:-4]]
  df = dfs0[s.name]
  index_cols = ["dept code","year","item categ"]
  if c.subsample > 1: # TODO !? WTF is this conditional necessary?
    df = ( df . groupby( index_cols ) .
           apply( lambda df:
                  prepend_avg_muni(
                    index_cols, s.money_cols, df ) ) .
           drop( columns = index_cols ) .
           reset_index() .
           drop( columns = "level_3" ) )
  else:
    # start diverge
    pass

for s in [s4.series_pct[1]]: # Works for 0 but not 1!
    df = dfs0[s.name]
    # end diverge
    df = ( df . groupby( index_cols ) .
           apply( lambda df:
                  prepend_avg_muni(
                    index_cols, s.money_cols, df ) ) .
           reset_index() .
           drop( columns = "level_3" ) )
