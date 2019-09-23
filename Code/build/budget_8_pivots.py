if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.metadata.terms as t
  import Code.util.misc as util
  import Code.util.aggregate_all_but_biggest as defs
  import Code.metadata.two_series as ser

if True:
  group_vars = ["dept", "muni", "year"]
  geo_vars   = ["dept", "muni", "dept code", "muni code"]
  assert c.subsample == 1 # This program expects the full sample.

if True: # read data
  raw = {}
  for s in ser.series:
    raw[s.name] = (
      pd.read_csv(
        ( "output/budget_7_verbose/recip-" + str(c.subsample)
          + "/" + s.name + ".csv") ) .
      sort_values( group_vars ) )

write_pivots( dept = "AMAZONAS", muni = "LETICIA", "index_col"

def write_pivots( dept : str,
                  muni : str,
                  dept_code : int,
                  muni_code : int,
                  index_col : str,
                  columns_col : str,
                  all_places : pd.DataFrame
                  ) -> pd.DataFrame:
  """ PITFALL: Does IO *and* returns a value."""
  dest = "output/pivots/" + dept + "/" + muni
  if not os.path.exists(dest): os.makedirs(dest)
  place = ( all_places
            [ (all_places["muni"] == muni) &
              (all_places["dept"] == dept) ] .
            copy() )
  p = place.pivot( index = index_col,
                   columns = columns_col,
                   values = money )
  p.to_csv( dest + "/" + f + ".csv" )
  return p

#for where in ["LETICIA"]:
#  for (f,money) in [(t.ingresos,"item total"),
#                    (t.gastos, "item oblig")]:
#    dest = "output/pivots/" + where
#    if not os.path.exists( dest ):
#      os.makedirs( dest )
#    df = raw[f]
#    df = df[ df["muni"] == where ].copy()
#    p = df.pivot( index = "item categ",
#                  columns = "year",
#                  values = money )
#    p.to_csv( dest + "/" + f + ".csv" )

