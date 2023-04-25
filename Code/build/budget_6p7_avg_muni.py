# PURPOSE:
# In the -pct files, compute an "average municipality"
# for each district.

if True:
  import os
  from typing import List,Set,Dict
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.terms as t
  from Code.util.misc import to_front
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
  dfs0, dfs1 = {}, {} # input, output
  for s in s4.series:
    dfs0[s.name] = pd.read_csv (
      os.path.join ( source,
                     s.name + ".csv" ) )

if True: # count munis per department
  # PITFALL: The number depends on the subsample size being used.
  # That's why we can't just use the data from build.use_keys.geo
  # PITFALL: Not every muni has data for every year in every file.
  # That's why there are two data sets, one for ingresos and one for gastos,
  # and why we count muni-years as well as munis.
  # PITFALL: Later (in stage 9, "static compare")
  # we take the average of years > 2015,
  # which is why we only count those years here.
  counts = {}
  for s in s4.series_pct:
    pre_counts = (
      dfs0[s.name]
      [["dept code","muni code","year"]] )
    pre_counts = ( # discard dept-level rows
      pre_counts . loc[
        pre_counts["muni code"] > 0 ] )
    pre_counts["count"] = 1
    muni_counts = (
      pre_counts
      [["dept code","muni code","count"]] .
      drop_duplicates() .
      groupby( "dept code" ) .
      agg('sum')
      ["count"] )
    muni_year_counts = (
      pre_counts
      [pre_counts["year"] > 2015]
      [["dept code","muni code","year","count"]] .
      drop_duplicates() .
      groupby( ["dept code"] ) .
      agg('sum')
      ["count"] )
    counts[s.name] = pd.concat( [ muni_counts,
                                  muni_year_counts],
                                axis = "columns" )
    counts[s.name].columns = ["munis","muni-years"]
  def get_muni_count( fn, dc : int ) -> int:
    return ( int( counts[fn] .
                  loc[ dc, "munis" ] )
             if dc in muni_counts.index
             else 1 ) # TODO ? ugly, ought to be Optional.
    # (Would return Nothing for depts with only dept-level info.)
  def get_muni_year_count( fn, dc : int ) -> int:
    return ( int( counts[fn] .
                  loc[ dc, "muni-years" ] )
             if dc in muni_counts.index
             else 3 ) # TODO ? ugly, ought to be Optional.
    # (Would return Nothing for depts with only dept-level info.)

if True: # Define how to compute the average non-dept muni
         # in some (dept,year,item categ) cell.
  def prepend_avg_muni( index_cols : List[str],
                        money_cols : List[str],
                        munis_in_dept : int,
                        muni_years_in_dept : int,
                        df0 : pd.DataFrame,
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
    avg = df.iloc[0] . copy()
    avg["muni code"] = -2 # TODO ? Ugly.
    avg[money_cols] = ( # The missing-rows-aware mean.
      df[money_cols] . sum() /
      munis_in_dept )
    res = ( pd.concat( [ pd.DataFrame([avg]),
                         df0],
                       axis="rows",
                       sort=True ) . # because unequal column orders
            drop(columns = ["index"] ) )
    res["munis in dept"] = munis_in_dept
    res["muni-years in dept"] = muni_years_in_dept
    return res
  if True:
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
    z = ( prepend_avg_muni( ["dept code"], ["money","cash"], 4, 8, x) .
          reset_index(drop=True) )
    for cn in y.columns:
      assert y[cn].equals(z[cn])
    del(x,y,z)

index_cols = ["dept code","year","item categ"]
for s in s2.series: # Add average muni to the to -pct data sets.
  dfs1[s.name] = ( # Handle the peso-valued data sets.
    dfs0[s.name] )
  spct = s.name + "-pct"
  if True: # Handle the %-valued data sets.
    df = dfs0[ spct ]
    df["dc"] = df["dept code"] # TODO ? ugly
    dfs1[spct] = to_front(
      ["dept code","muni code"],
      ( df . groupby( index_cols ) .
        apply( lambda df:
               prepend_avg_muni(
                 index_cols,
                 s.money_cols,
                 get_muni_count(      spct, df["dc"].iloc[0] ),
                 get_muni_year_count( spct, df["dc"].iloc[0] ),
                 df ) .
               drop( columns = index_cols ) ) .
        reset_index() .
        drop( columns = ["dc","level_3"] ) ) )

if True: # tests
  assert dfs0["gastos"]   .equals( dfs1["gastos"] )
  assert dfs0["ingresos"] .equals( dfs1["ingresos"] )
  for s in s4.series_pct: # test dimensions
    pct_series =     dfs1[ s.name      ]
    non_pct_series = dfs1[ s.name[:-4] ] # drop the "-pct" suffix
    assert ( pct_series.columns .
             drop( ["munis in dept",
                    "muni-years in dept"] ) .
             equals(
               non_pct_series.columns ) )
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
