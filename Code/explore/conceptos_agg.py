# To determine whether the (muni,year,concepto)-aggregated data makes sense.

# import Code.explore.conceptos_agg as eca
from itertools import chain
import numpy as np
import pandas as pd
import Code.util as util
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


# columns defining the unit of observation
columns_uob = ["muni","year","codigo","codigo-top"]

dfs = {}
for s in sm.series:
  dfs[s] = pd.read_csv( "output/conceptos_3_agg/" + s + ".csv" )

ing = dfs["ingresos"]
inv = dfs["inversion"]
fun = dfs["funcionamiento"]

def summarize_col( col : str, df : pd.DataFrame ) -> pd.DataFrame:
  theRange = df[col].max() - df[col].min()
  theMin = df[col].min()
  theMax = df[col].max()
  theRatio = 0 if theRange == 0 else theRange / theMin
  return pd.DataFrame( { ( col + "range") : [theRange]
                       , ( col + "min"  ) : [theMin]
                       , ( col + "max"  ) : [theMax]
                       , ( col + "ratio") : [theRatio] } )

df = ing
x = ( df .
  groupby( by = ["muni","year","codigo"] ) .
  apply( lambda df :
         summarize_col( "Presupuesto Definitivo",
                        df) ) )
#   reset_index() .
#   drop( columns = ["level_3"] ) )

df["Presupuesto Inicial"].max()
df["Presupuesto Inicial"].min()
x["ratio"].min()
x["ratio"].max()
x[ x["ratio"] == np.inf ]
len( x[ x["max"] < 0.5 ] )
x[ x["max"] > 1 ].min()

# ingresos -- looks good. max ratio (of presupuestal inicial)  is infinity, but those are 0.01 pesos / 0 pesos
