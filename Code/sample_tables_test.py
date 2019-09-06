if True:
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.series_metadata as ser
  import Code.sample_tables_defs as defs


######
###### Unit test
######

realish_data = (
  # Real-ish in the sense that there are multiple group columns,
  # and a string variable that is meaningless when summed.
  pd.DataFrame( {
    "where" : [5,5,5,5,           6,6,6,6,          5,5,5,5],
    "when"  : [1,1,1,1,           1,1,1,1,          2,2,2,2],
    "item"  : ["0","1","2","3",  "0","1","2","3",  "0","1","2","3"],
    "value" : [0,1,2,3,           10,11,12,13,      0,-1,-2,-3] } ) )

assert (
  defs .
  sum_all_but_greatest_n_rows_in_groups(
    2, ["where","when"], ["value"], ["item"], realish_data )
  [["where","when","item","value"]] .
  reset_index( drop = True ) .
  equals( pd.DataFrame(
    { "where" : [5,5,5,           5,5,5,            6,6,6],
      "when"  : [1,1,1,           2,2,2,            1,1,1],
      "item"  : [np.nan,"2","3",  np.nan,"1","0",  "2","3",np.nan],
      "value" : [1,2,3,          -5,-1,0,           12,13,21] } ) ) )


######
###### Integration test
######

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

