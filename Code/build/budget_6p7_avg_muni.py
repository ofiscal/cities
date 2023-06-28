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
  import Code.build.budget_6p7_avg_muni_lib as lib
  import Code.build.use_keys        as uk
  import Code.common                as c
  import Code.metadata.four_series  as s4
  import Code.metadata.terms        as t
  import Code.metadata.two_series   as s2
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
  # we take the average over years in the current administration,
  # which is why we only count those years here.

  dept_level_counts : Dict [str, pd.DataFrame] = {}
    # The index of each `DataFrame` in `dept_level_counts`
    # will be the dept code,
    # due to the groupby statements below.
    # The column names in each will be ["munis", "muni-years"].
  for s in s4.series_pct: # Populate `dept_level_counts`.
    pre_counts = (
      dfs0 [s.name]
      [["dept code","muni code","year"]]
      . drop_duplicates() )
    pre_counts = ( # discard dept-level rows
      pre_counts . loc [
        pre_counts ["muni code"] > 0 ] )
    pre_counts ["count"] = 1
    muni_counts : pd.Series = (
      # Count distinct munis.
      # If a muni appears in any year, it is counted.
      # TODO ? Should this only include years during this admin?
      pre_counts
      . drop ( columns = ["year"] )
      . drop_duplicates ()
      . groupby ( "dept code" )
      . agg ('sum')
      ["count"] )
    muni_year_counts : pd.Series = (
      # Count distinct muni-years during this admin.
      pre_counts
      [ pre_counts ["year"] >= c.admin_first_year ]
      . groupby ( ["dept code"] )
      . agg ('sum')
      ["count"] )
    dept_level_counts [s.name] = pd.concat ( [ muni_counts,
                                               muni_year_counts ],
                                             axis = "columns" )
    dept_level_counts [s.name] . columns = ["munis","muni-years"]


if True: # Define how to compute the average non-dept muni
         # in some (dept,year,item categ) cell.
  def prepend_avg_muni (
      index_cols         : List [str],
        # `index_cols` is an argument only to make testing easier.
        # In the test it has length 1 (it is ["dept code"]).
        # In production it has length 3: ["dept code","year","item categ"].
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
    avg ["muni code"] = -2 # TODO ? Ugly, requires special interpretation:
      # Most muni codes really are muni codes, but -2 means "dept average".
    avg [money_cols] = ( # The missing-rows-aware mean.
      df [money_cols] . sum () /
      # TODO ! This divisor could depend on the year.
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
    z = (
      prepend_avg_muni ( index_cols = ["dept code"],
                         money_cols = ["money","cash"],
                         munis_in_dept = 4,
                         muni_years_in_dept = 8,
                         df0 = x)
      . reset_index ( drop = True ) )
    for cn in y.columns:
      assert y [cn] . equals (
             z [cn] )
    del (x,y,z)

index_cols = ["dept code","year","item categ"]
for s in s2.series: # Add average muni to the to -pct data sets.
  dfs1 [s.name] = ( # Copy only two (the peso-valued ones)
    # of the four data sets from dfs0.
    # PITFALL: This "copy" is by reference,
    # which is (faster, and) fine because they aren't modified.
    dfs0 [s.name] )
  spct = s.name + "-pct"
  if True: # Create the other two (the %-valued) data sets.
    df = dfs0 [ spct ] . copy ()
    df ["dc"] = df ["dept code"] # TODO ? Ugly, but seems unavoidable. Why:
      # The `groupby` below absorbs "dept code" into grouped data index.
      # The `apply` that follows it needs to use the department code, but
      # none of the individual frames has access to the grouped data index.
      # "dc", a copy of "dept code", thus conveys it to `prepend_avg_muni`.
    dfs1 [spct] = to_front (
      ["dept code","muni code"],
      ( df . groupby ( index_cols ) .
        apply (
          lambda df: prepend_avg_muni (
            index_cols         = index_cols,
            money_cols         = s.money_cols,
            munis_in_dept      = lib.get_muni_count (
              dept_level_counts = dept_level_counts,
              muni_counts       = muni_counts,
              filename          = spct,
              dept_code         = df["dc"].iloc[0] ),
            muni_years_in_dept = lib.get_muni_year_count (
              dept_level_counts = dept_level_counts,
              muni_counts       = muni_counts,
              filename          = spct,
              dept_code         = df["dc"].iloc[0] ),
            df0 = df )
          . drop ( columns = index_cols ) ) .
        reset_index () .
        drop ( columns = ["dc","level_3"] ) ) )

if True: # tests
  assert dfs0 ["gastos"]   is dfs1 ["gastos"]
  assert dfs0 ["ingresos"] is dfs1 ["ingresos"]

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

  if c.subsample == 1: # In full sample, every dept is present
                       # in both `DataFrame`s in `dept_level_counts`.
    geo = uk.geo[["dept code"]] . drop_duplicates()
    geo["one"] = 1
    for k in dept_level_counts.keys():
      i = dept_level_counts [k] . index
      assert i . equals ( i . drop_duplicates () )
      df = pd.DataFrame ( { "dept code" : i } )
      df = df.merge ( geo, on = "dept code" )
      assert ( geo["one"] . sum() ==
               df ["one"] . sum() )

for s in s4.series: # Save the result.
  dfs1 [s.name] . to_csv (
    os.path.join ( dest,
                   s.name + ".csv" ),
    index = False ) # TODO : Right? I just added this line, and haven't tested it. It might break a test.
