# PURPOSE:
# In the -pct files, compute an "average municipality"
# for each district.
#
# PITFALL:
# Doing similarly for the peso-valued files seems less useful.
# If money remained measured in levels rather than logs,
# municipal budgets vary so widely that small-muni budget
# variation could be rendered nearly invisible.
# Using logs is also problematic,
# because then the sum of the average budget item
# is unequal to the average municipal budget.)

if True:
  import os
  import pandas                     as pd
  from   typing import List, Set, Dict
  #
  import Code.common                as c
  import Code.metadata.four_series  as s4
  import Code.metadata.two_series   as s2
  import Code.metadata.terms        as t
  from   Code.util.misc import to_front


if True: # folders
  source = os.path.join ( c.outdata,
                          "budget_6p5_cull_and_percentify",
                          "recip-" + str (c.subsample) )
  dest   = os.path.join ( c.outdata,
                          "budget_6p7_avg_muni",
                          "recip-" + str(c.subsample) )
  if not os.path.exists ( dest ):
    os.makedirs (         dest )

if True: # input data
  dfs0, dfs1 = {}, {} # input, output
  for s in s4.series:
    dfs0 [s.name] = pd.read_csv (
      os.path.join ( source,
                     s.name + ".csv" ) )

if True: # Count munis per department.
  #
  # PITFALL: The number depends on the subsample size being used.
  # That's why we can't just use the data from build.use_keys.geo
  #
  # PITFALL: Not every muni has data for every year in every file.
  # That's why there are two data sets, one for ingresos and one for gastos,
  # and why we count muni-years as well as munis.
  #
  # PITFALL: Later (in stage 9, "static compare")
  # we take the average of years > 2015,
  # which is why we only count those years here.

  counts : Dict [str, pd.DataFrame] = {}
    # The index of each `DataFrame` in `counts` will be the dept code,
    # due to the groupby statements below.
  for s in s4.series_pct:
    pre_counts = (
      dfs0 [s.name]
      [["dept code","muni code","year"]] )
    pre_counts = ( # discard dept-level rows
      pre_counts . loc[
        pre_counts ["muni code"] > 0 ] )
    pre_counts ["count"] = 1
    muni_counts = ( # Count distinct munis.
      # If a muni appears in any year, it is counted.
      pre_counts
      . drop ( columns = ["year"] )
      . drop_duplicates ()
      . groupby ( "dept code" )
      . agg ('sum')
      ["count"] )
    muni_year_counts = ( # Count distinct muni-years post-2015.
      pre_counts
      [ pre_counts ["year"] > 2015]
      . drop_duplicates ()
      . groupby ( ["dept code"] )
      . agg ('sum')
      ["count"] )
    counts [s.name] = pd.concat ( [ muni_counts,
                                    muni_year_counts ],
                                  axis = "columns" )
    counts [s.name] . columns = ["munis","muni-years"]

  def get_muni_count ( filename : str,
                       dept_code : int
                      ) -> int:
    """A helper function for getting data from `counts`."""
    return ( int ( counts [filename] .
                   loc [ dept_code, "munis" ] )
             if dept_code in muni_counts . index
             else 1 ) # TODO ? ugly, ought to be Optional.
  # (In that case I would return Nothing for depts with only dept-level info.)
  #
  # TODO : Is this even right? I seem to be assuming the muni is present,
  # even if it's not in the count.
  # Maybe it's because the default value is only relevant in subsamples,
  # i.e. for testing?

  def get_muni_year_count ( filename : str,
                            dept_code : int
                           ) -> int:
    """A helper function for getting data from `counts`."""
    return ( int ( counts [filename] .
                  loc [ dept_code, "muni-years" ] )
             if dept_code in muni_counts . index
             else 3 ) # TODO ? ugly, ought to be Optional.
  # (In that case I would return Nothing for depts with only dept-level info.)
  #
  # TODO : Is this even right? I seem to be assuming the muni is present,
  # in every year, even if it's not in the count.
  # Maybe it's because the default value is only relevant in subsamples,
  # i.e. for testing?

if True: # Define how to compute the average non-dept muni
         # in some (dept,year,item categ) cell.
  def prepend_avg_muni (
      index_cols         : List [str], # Sometimes length 1 ["dept code"],
                                       # sometimes length > 1.
      money_cols         : List [str], # What to average.
      munis_in_dept      : int,
      muni_years_in_dept : int,
      df0                : pd.DataFrame, # A slice with constant
                                         # (dept,year,item categ).
  )                     -> pd.DataFrame: # `df0` plus a new "average" muni,
                                         # computed omitting the dept row.
    df = ( df0 . copy ()
           [ df0 ["muni code"] != 0 ] .
          reset_index () )
    if len (df) == 0: return df0
      # If there is no muni-level info, only dept-level
      # (true in some subsamples), leave the input unchanged;
      # don't try to add an average municipality.

    avg = df.iloc [0] . copy ()
    avg ["muni code"] = -2 # TODO ? Ugly.
    avg [money_cols] = ( # The missing-rows-aware mean.
      df [money_cols] . sum () /
      munis_in_dept )
    res = ( pd.concat ( [ pd.DataFrame ( [avg] ),
                          df0 ],
                       axis = "rows",
                       sort = True ) . # because unequal column orders
            drop ( columns = ["index"] ) )
    res ["munis in dept"] = munis_in_dept
    res ["muni-years in dept"] = muni_years_in_dept
    return res

  if True: # Test `prepend_avg_muni`.
    x = pd.DataFrame ( [ [99,  0, 1,  2, 1],
                         [99,  1, 1, 65, 2],
                         [99,  2, 5, 15, 3] ],
                       columns = [ "dept code", "muni code",
                                   "money","cash","pecan" ] )
    y = ( pd.DataFrame ( [ [99, -2, 1.5, 20, 2],
      # The previous row (the only new one) has
      # average money = (1+5)   / 4 (because dept 99 has 4 munis)
      # average cash  = (15+65) / 4 (because dept 99 has 4 munis)
      # and is otherwise just like the muni with code 1.
                           [99,  0, 1,    2, 1],
                           [99,  1, 1,   65, 2],
                           [99,  2, 5,   15, 3] ],
                        columns = [ "dept code", "muni code",
                                    "money","cash","pecan" ] ) .
          astype (float) )
    z = ( prepend_avg_muni ( ["dept code"], ["money","cash"], 4, 8, x) .
          reset_index ( drop = True ) )
    for cn in y.columns:
      assert y [cn] . equals (
             z [cn] )
    del (x,y,z)

index_cols = ["dept code","year","item categ"]
for s in s2.series: # Add average muni to the to -pct data sets.
  dfs1 [s.name] = ( # Handle the peso-valued data sets.
    dfs0 [s.name] )
    # TODO ? The above looks like it should be a copy.
  spct = s.name + "-pct"
  if True: # Handle the %-valued data sets.
    df = dfs0 [ spct ]
    df ["dc"] = df ["dept code"] # TODO ? ugly
    dfs1 [spct] = to_front (
      ["dept code","muni code"],
      ( df . groupby ( index_cols ) .
        apply ( lambda df:
                prepend_avg_muni (
                  index_cols,
                  s.money_cols,
                  get_muni_count      ( spct, df["dc"].iloc[0] ),
                  get_muni_year_count ( spct, df["dc"].iloc[0] ),
                  df ) .
                drop ( columns = index_cols ) ) .
        reset_index () .
        drop ( columns = ["dc","level_3"] ) ) )

if True: # tests
  assert dfs0 ["gastos"]   . equals ( dfs1 ["gastos"] )
  assert dfs0 ["ingresos"] . equals ( dfs1 ["ingresos"] )
  for s in s4.series_pct: # test dimensions
    pct_series =     dfs1 [ s.name       ]
    non_pct_series = dfs1 [ s.name [:-4] ] # drop the "-pct" suffix
    assert ( pct_series.columns .
             drop ( [ "munis in dept",
                      "muni-years in dept" ] ) .
             equals (
               non_pct_series.columns ) )
    nAverages = len (
      non_pct_series
      [ non_pct_series ["muni code"] != 0 ] .
         # The logic behind needing to include the preceding line
         # is complicated; see budget_6p7_avg_muni.md
      groupby ( ["dept code","year","item categ"] ) .
      apply ( lambda _: () ) )
    assert len (pct_series) == nAverages + len (non_pct_series)

for s in s4.series: # Save the result.
  dfs1 [s.name] . to_csv (
    os.path.join ( dest,
                   s.name + ".csv" ),
    index = False ) # TODO : Right? I just added this line, and haven't tested it. It might break a test.
