import numpy as np
import pandas as pd

import Code.common as c
import Code.util as util
import Code.metadata.four_series as sm
import Code.build.budget_3_dept_muni_year_item_defs as defs


disagg = "output/budget_2_subsample/recip-"       + str(c.subsample)
agg    = "output/budget_3_dept_muni_year_item/recip-" + str(c.subsample)

group_fields = ["year","muni code","item code"]

dfs,dfas = ({},{})
for s in sm.series:
  dfs[s] = pd.read_csv( disagg + "/" + s + ".csv",
                        encoding = "utf-8" )
  dfas[s] = pd.read_csv( agg + "/" + s + ".csv",
                         encoding = "utf-8" )

def at_spot( spot : pd.DataFrame,
             df : pd.DataFrame ) -> pd.DataFrame:
  return df[ ( df[group_fields] == spot ) .
             all( axis = 'columns' ) ]

def spot_test( n : int ):
  """ No matter what value of n one chooses,
  the resulting slice from each of the input data sets should have
  no more rows than the slice from the corresponding output data set,
  and the latter should have only one row.

  Aggregation seems only to reduce the number of rows in funcionamiento.
  In the other data sets, once we have narrowed to the rows of interest,
  the value taken over group_fields
  is already unique across observations. """
  for s in sm.series:
    df = dfs[s]
    dfa = dfas[s]
    spot = df.iloc[n][group_fields]
      # A "spot" is an assignment of values to group_fields.
    print( "\n" + s + "\n" )
    print( at_spot( spot, df ) )
    print( at_spot( spot, dfa ) )

dfs["inversion"][group_fields].sort_values(group_fields)
