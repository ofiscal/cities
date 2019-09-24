if True:
  import os
  import pandas as pd
  #
  import Code.common as c
  import Code.util.aggregate_all_but_biggest as defs
  import Code.metadata.two_series as ser

assert c.subsample == 1 # This program only works on the full sample.

if True:
  spacetime = ["dept", "muni", "year", "dept code", "muni code"]
  space   = ["dept", "muni", "dept code", "muni code"]

if True: # read data
  raw = {}
  for s in ser.series:
    raw[s.name] = (
      pd.read_csv(
        ( "output/budget_7_verbose/recip-" + str(c.subsample)
          + "/" + s.name + ".csv") ) .
      sort_values( spacetime ) )

if True: # in each spacetime slice, lump all but the biggest 5
         # expenditures into a single observation
  grouped = {}
  for s in ser.series:
    grouped[s.name] = (
      defs.sum_all_but_greatest_n_rows_in_groups(
        n = 5,
        group_vars = spacetime,
        sort_vars = s.peso_cols,
        meaningless_to_sum = ["item categ"],
        df0 = raw[s.name] ) )

def write_pivots( dept : str,
                  muni : str,
                  values_col : str,
                  all_places : pd.DataFrame,
                  filename : str
                  ) -> pd.DataFrame:
  """ PITFALL: Writes a file *and* returns a value."""
  dest = ( "output/pivots/recip-" + str(c.subsample) +
           "/" + dept + "/" + muni )
  if not os.path.exists(dest): os.makedirs(dest)
  place = ( all_places
            [ (all_places["muni"] == muni) &
              (all_places["dept"] == dept) ] .
            copy() )
  p = place.pivot( index = "item categ",
                   columns = "year",
                   values = values_col )
  p.to_csv( dest + "/" + filename + ".csv" )
  return p

for s in ser.series:
  ( grouped[s.name] .
    groupby( space ) .
    apply(
      lambda df:
      write_pivots(
        dept = df.iloc[0]["dept"],
        muni = df.iloc[0]["muni"],
        values_col = s.peso_cols[0],
        all_places = df,
        filename = s.name ) ) )

