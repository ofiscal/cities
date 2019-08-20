# To determine whether the (muni,year,concepto)-aggregated data makes sense.

# import Code.explore.conceptos_agg as eca
import numpy as np
import pandas as pd

import Code.common as c
import Code.build.sisfut_metadata as sm


# columns defining the unit of observation
columns_uob = ["muni code","year","item categ","item top"]

dfs = {}
for s in sm.series:
  dfs[s] = pd.read_csv(
    "output/conceptos_3_agg/recip-" + str(c.subsample) +
    "/" + s + ".csv" )

ing = dfs["ingresos"]
inv = dfs["inversion"]
fun = dfs["funcionamiento"]

def summarize_col( col : str, df : pd.DataFrame ) -> pd.DataFrame:
  theRange = df[col].max() - df[col].min()
  theMin = df[col].min()
  theMax = df[col].max()
  theRatio = 0 if theRange == 0 else theRange / theMin
  return pd.DataFrame( { ( col + ", range") : [theRange]
                       , ( col + ", min"  ) : [theMin]
                       , ( col + ", max"  ) : [theMax]
                       , ( col + ", ratio") : [theRatio] } )

df = ing
x = ( df .
  groupby( by = ["muni code","year","item categ"] ) .
  apply( lambda df :
         summarize_col( "item def", df) ) .
   reset_index() .
   drop( columns = ["level_3"] ) )

df["item def"].max()
df["item def"].min()
x["item def, ratio"].min()
x["item def, ratio"].max()
x[ x["item def, ratio"] == np.inf ]
len( x[ x["item def, max"] < 0.5 ] )
x[ x["item def, max"] > 1 ].min()

# ingresos -- looks good. max ratio (of presupuestal inicial)  is infinity, but those are 0.01 pesos / 0 pesos
