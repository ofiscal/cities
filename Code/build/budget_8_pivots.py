# PURPOSE:
# Generates a lot of little data sets, in a file tree.
# The columns of each data (except the first) set are years,
# and the rows are budget items.
# The structure of the filetree is best described by example:
#
#   [output/2023/pivots/recip-100/CAUCA/MORALES]$ ls *.csv -1
#   gastos.csv              # in COP
#   gastos-pct.csv          # in percentages
#   ingresos.csv            # in COP
#   ingresos-pct.csv        # in percentages
#
# (Each folder also includes equivalent .xlsx files.)

if True:
  from   os import path, makedirs
  import pandas as pd
  from   pathlib import Path
  from   typing import List,Set,Dict
  #
  import Code.common                as c
  import Code.metadata.four_series  as s4
  import Code.util.aggregate_all_but_biggest.better \
    as agger # "aggregator"


dest_root = path.join ( c.outdata, "pivots",
                        "recip-" + str (c.subsample) )

if True:
  spacetime = ["dept", "muni", "year", "dept code", "muni code"]
  space     = ["dept", "muni",         "dept code", "muni code"]

if True: # Read data.
  ungrouped : Dict [str, pd.DataFrame] = {}
  for s in s4.series:
    ungrouped [s.name] = (
      pd.read_csv (
        ( path.join ( c.outdata,
                      "budget_7_verbose",
                      "recip-" + str (c.subsample),
                      s.name + ".csv" ) ) ) .
      sort_values ( spacetime ) )

if True: # In each spacetime slice, lump every expenditure which is
         # not among the top five expenditures for some year
         # into a single observation.
  grouped : Dict [str, pd.DataFrame] = {}
  for s in s4.series:
    grouped [s.name] = (
      agger.go (
        five = 5,
        space_cols = space, # PITFALL: Include (dept code,muni code),
          # not just (dept,muni), to avoid summing the codes.
        time_col = "year",
        categ_col = "item categ",
        money_col = s.money_cols [0],
        df = ungrouped [s.name] ) )

def write_pivots ( dept : str,
                   muni : str,
                   values_col : str,
                   all_places : pd.DataFrame,
                   filename : str
                  ) -> pd.DataFrame:
  """ PITFALL: Writes a file *and* returns a value."""
  dest = path.join ( dest_root, dept, muni )
  if not path.exists (dest): makedirs (dest)
  place = ( all_places
            [ ( all_places ["muni"] == muni ) &
              ( all_places ["dept"] == dept ) ] .
            copy () )
  p = place.pivot ( index = "item categ",
                    columns = "year",
                    values = values_col )
  p.to_csv   ( path.join ( dest, filename + ".csv"  ) )
  p.to_excel ( path.join ( dest, filename + ".xlsx" ) )
  return p

for s in s4.series:
  ( grouped [s.name] .
    groupby (space) .
    apply (
      lambda df:
      write_pivots (
        dept = df.iloc [0] ["dept"],
        muni = df.iloc [0] ["muni"],
        values_col = s.money_cols [0],
        all_places = df,
        filename = s.name ) ) )

( Path (
    path.join ( dest_root,
                "timestamp-for-pivot-tables" ) )
  . touch () )
