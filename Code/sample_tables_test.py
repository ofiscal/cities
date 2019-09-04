if True:
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.series_metadata as ser


if True: # read input data
  dis = {}
  for s in ser.series:
    dis[s.name] = pd.read_csv(
      ( "output/budget_7_verbose/recip-" + str(c.subsample)
        + "/" + s.name + ".csv"),
      encoding = "utf-16" )

if True: # read output data
  dos = {}
  for s in ser.series:
    dos[s.name] = pd.read_csv(
      ( "output/sample_tables/recip-" + str(c.subsample)
        + "/" + s.name + ".csv"),
      encoding = "utf-16" )

group_vars = ["dept","muni","year"]
for n in ["gastos"]:
  di,do = dis[n], dos[n]

spot = di.iloc[-1][group_vars]
def at_spot( spot, df ):
  return df[ (df[group_vars] == spot).transpose().all() ]

### RESUME HERE: Problem: The "other" column is a sum that includes
### the broken out rows as well as the ones I intended to include.
bogota_in = ( at_spot( spot, di )
              [ group_vars + ["item code","item oblig"]] .
              sort_values( group_vars + ["item oblig"] ) )
at_spot( spot, do )[ group_vars + ["item code","item oblig"]]
bogota_in["item oblig"].sum()
