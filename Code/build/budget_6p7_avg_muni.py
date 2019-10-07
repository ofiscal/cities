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
  import Code.metadata.four_series as s4

if True: # folders
  source = "output/budget_6p5_cull_and_percentify/recip-" + str(c.subsample)
  dest   = "output/budget_6p7_avg_muni/recip-"            + str(c.subsample)
  if not os.path.exists( dest ):
    os.makedirs(         dest )

if True: # input data
  geo = ( uk.depts_and_munis
         [["dept code","muni code","munis"]] )
  dfs = {}
  for s in s4.series:
    dfs[s.name] = pd.read_csv(
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
           [df0["muni code"] != -1] .
          reset_index() )
    assert len(df) > 0
      # Fails if dept has no muni-level info.
      # (Bogotá comes close: it has no "dept"-level info.)
    munis_in_dept = int(
        geo.loc[ ( geo       ["dept code"] ==
                   df.iloc[0]["dept code"] ),
                 "munis" ] .
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
    # Department 99 has 4 municipalities.
    x = pd.DataFrame( [ [99, -1, 1, 2, 1],
                        [99,  1, 1, 65, 2],
                        [99,  2, 5, 15, 3] ],
                      columns = ["dept code", "muni code",
                                 "money","cash","pecan"] )
    y = ( pd.DataFrame( [ [99, -2, 1.5, 20, 2],
      # The previous row (the only new one) has
      # average money=(1+5) / 4,
      # average cash=(15+65) / 4,
      # and is otherwise just like the muni with code 1.
                          [99, -1, 1,    2, 1],
                          [99,  1, 1,   65, 2],
                          [99,  2, 5,   15, 3] ],
                        columns = ["dept code", "muni code",
                                   "money","cash","pecan"] ) .
          astype(float) )
    z = ( prepend_avg_muni( ["dept code"], ["money","cash"], x) .
          reset_index(drop=True) )
    for cn in y.columns:
      assert y[cn].equals(z[cn])

for s in s4.series_pct:
  df = dfs[s.name]
  index_cols = ["dept code","year","item categ"]
  df = to_front(
    ["dept code","muni code"],
    ( df . groupby( index_cols ) .
      apply( lambda df:
             prepend_avg_muni( index_cols, s.money_cols, df ) .
             drop( columns = index_cols ) ) .
      reset_index() .
      drop( columns = ["level_3"] ) ) )
  dfs[s.name] = df

for s in s4.series_pct:
  pct_series =     dfs[ s.name      ]
  non_pct_series = dfs[ s.name[:-4] ]
  nDepts = len(
    pct_series .
    groupby( ["dept code","year","item categ"] ) .
    apply( lambda _: () ) )
  assert len(pct_series) == nDepts + len(non_pct_series)
  assert pct_series.columns.equals(
     non_pct_series.columns )
 
for s in s4.series:
  dfs[s.name].to_csv( dest + "/" + s.name + ".csv" )

