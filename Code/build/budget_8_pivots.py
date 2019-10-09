if True:
  from typing import List,Set,Dict
  import os
  from pathlib import Path
  import pandas as pd
  #
  import Code.common as c
  import Code.util.aggregate_all_but_biggest.better \
    as agger # "aggregator"
  import Code.metadata.four_series as s4

dest_root = "output/pivots/recip-" + str(c.subsample)

if True:
  spacetime = ["dept", "muni", "year", "dept code", "muni code"]
  space     = ["dept", "muni",         "dept code", "muni code"]

if True: # read data
  ungrouped : Dict[str, pd.DataFrame] = {}
  for s in s4.series:
    ungrouped[s.name] = (
      pd.read_csv(
        ( "output/budget_7_verbose/recip-" + str(c.subsample)
          + "/" + s.name + ".csv") ) .
      sort_values( spacetime ) )

if True: # in each spacetime slice, lump every expenditure which is
         # not among the top five expenditures for some year
         # into a single observation
  grouped : Dict[str, pd.DataFrame] = {}
  for s in s4.series:
    grouped[s.name] = (
      agger.go(
        five = 5,
        space_cols = space, # PITFALL: include (dept code,muni code),
          # not just (dept,muni), to avoid summing the codes.
        time_col = "year",
        categ_col = "item categ",
        money_col = s.money_cols[0],
        df = ungrouped[s.name] ) )

def write_pivots( dept : str,
                  muni : str,
                  values_col : str,
                  all_places : pd.DataFrame,
                  filename : str
                  ) -> pd.DataFrame:
  """ PITFALL: Writes a file *and* returns a value."""
  dest = ( dest_root + "/" + dept + "/" + muni )
  if not os.path.exists(dest): os.makedirs(dest)
  place = ( all_places
            [ (all_places["muni"] == muni) &
              (all_places["dept"] == dept) ] .
            copy() )
  p = place.pivot( index = "item categ",
                   columns = "year",
                   values = values_col )
  p.to_csv(   dest + "/" + filename + ".csv" )
  p.to_excel( dest + "/" + filename + ".xlsx" )
  return p

for s in s4.series:
  ( grouped[s.name] .
    groupby( space ) .
    apply(
      lambda df:
      write_pivots(
        dept = df.iloc[0]["dept"],
        muni = df.iloc[0]["muni"],
        values_col = s.money_cols[0],
        all_places = df,
        filename = s.name ) ) )

( Path( dest_root + "/" + "timestamp-for-pivot-tables" ) .
  touch() )

