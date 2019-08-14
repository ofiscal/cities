###### Based on the original three data sets from DNP
###### (ingreso, inversiones and funcionamiento), this builds three
###### similar data sets.
###### The unit of observation is the same, a "concepto",
###### i.e. an item of either expenditure or income.
###### Some new columns are added --
###### namely "year", "subcode" and "code=subcode".
###### Some verbose, redundant columns are omitted.

import pandas as pd
import Code.build.conceptos_1_defs as defs
import Code.build.sisfut_metadata as sm


dfs = defs.collect_raw()
dfs = defs.aggregated_item_codes( dfs )

for s in sm.series:
  dfs[s].to_csv( "output/conceptos_1/" + s + ".csv",
                 index = False )
