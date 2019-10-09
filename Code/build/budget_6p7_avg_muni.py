# PURPOSE:
# In the -pct files, compute an "average municipality"
# for each district.

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  #
  import Code.common as c
  from Code.util.misc import to_front
  import Code.build.use_keys as uk
  import Code.metadata.two_series as s2
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
  dfs0, dfs1 = {}, {} # input, output
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
        Average is only over munis; it omits the dept row.
"""
    df = ( df0.copy()
           [df0["muni code"] != 0] .
          reset_index() )
    if len(df) == 0: return df0
      # If there is no muni-level info, only dept-level
      # (true in some subsamples), leave the input unchanged;
      # don't try to add an average municipality.
    munis_in_dept = int(
        geo.loc[ ( geo       ["dept code"] ==
                   df.iloc[0]["dept code"] ),
                 "muni count" ] .
        head(1) )
    avg = df.iloc[0] . copy()
    avg["muni code"] = -2 # TODO ? Ugly.
    avg[money_cols] = ( # The missing-rows-aware mean.
        df[money_cols] . sum() / munis_in_dept )
    return ( pd.concat( [ pd.DataFrame([avg]),
                         df0],
                       axis="rows",
                       sort=True ) . # because unequal column orders
             drop(columns = ["index"] ) )
  if True: # test it
    x = pd.DataFrame( [ [99,  0, 1, 2, 1],
                        [99,  1, 1, 65, 2],
                        [99,  2, 5, 15, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","pecan"] )
    y = ( pd.DataFrame( [ [99, -2, 1.5, 20, 2],
      # The previous row (the only new one) has
      # average money = (1+5)   / 4 (because dept 99 has 4 munis)
      # average cash  = (15+65) / 4 (because dept 99 has 4 munis)
      # and is otherwise just like the muni with code 1.
                          [99,  0, 1,    2, 1],
                          [99,  1, 1,   65, 2],
                          [99,  2, 5,   15, 3] ],
                        columns = ["dept code", "muni code",
                                   "money","cash","pecan"] ) .
          astype(float) )
    z = ( prepend_avg_muni( ["dept code"], ["money","cash"], x) .
          reset_index(drop=True) )
    for cn in y.columns:
      assert y[cn].equals(z[cn])
    del(x,y,z)

for s in s2.series: # add average muni to the to -pct data sets
  index_cols = ["dept code","year","item categ"]
  df = dfs0[s.name].copy()
  dfs1[s.name] = df
  dfs1[s.name + "-pct"] = to_front(
    ["dept code","muni code"],
    ( df . groupby( index_cols ) .
      apply( lambda df:
             prepend_avg_muni( index_cols, s.money_cols, df ) .
             drop( columns = index_cols ) ) .
      reset_index() .
      drop( columns = ["level_3"] ) ) )

if True: # tests
  assert dfs0["gastos"]   .equals( dfs1["gastos"] )
  assert dfs0["ingresos"] .equals( dfs1["ingresos"] )
  for s in s4.series_pct: # test dimensions
    pct_series =     dfs1[ s.name      ]
    non_pct_series = dfs1[ s.name[:-4] ] # drop the "-pct" suffix
    assert pct_series.columns.equals(
       non_pct_series.columns )
    nAverages = len(
      non_pct_series
      [ non_pct_series["muni code"] != 0 ] .
         # The logic behind needing to include the preceding line
         # is complicated; see budget_6p7_avg_muni.md
      groupby( ["dept code","year","item categ"] ) .
      apply( lambda _: () ) )
    assert len(pct_series) == nAverages + len(non_pct_series)

for s in s4.series:
  dfs1[s.name].to_csv( dest + "/" + s.name + ".csv" )

