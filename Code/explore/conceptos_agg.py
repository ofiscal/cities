# To determine whether the (muni,year,concepto)-aggregated data makes sense.


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
  dfs[s] = pd.read_csv( "output/conceptos_2_agg/" + s + ".csv" )

#  dfg = ( df[s] .
#          groupby( columns_uob ) .
#          agg( ["min","max"] ) )

df = dfs["inversion"]
x = df.groupby( by = ["muni","year","codigo"] )
def f( col, df ):
  theRange = df[col].max() - df[col].min()
  theMin = df[col].min()
  theMax = df[col].max()
  theRatio = 0 if theRange == 0 else theRange / theMin
  return pd.DataFrame( { "range" : [theRange]
                       , "min"   : [theMin]
                       , "max"   : [theMax]
                       , "ratio" : [theRatio] } )

y = ( x .
  apply(lambda df: f("Presupuesto Definitivo",df) ) .
  reset_index() .
  drop( columns = ["level_3"] ) )

df["Presupuesto Inicial"].max()
df["Presupuesto Inicial"].min()
y["ratio"].min()
y["ratio"].max()
y[ y["ratio"] == np.inf ]
len( y[ y["max"] < 0.5 ] )
y[ y["max"] > 1 ].min()

# ingresos -- looks good. max ratio (of presupuestal inicial)  is infinity, but those are 0.01 pesos / 0 pesos
inversion
funcionamiento

x = pd.DataFrame( [[1,2],[2,2],[3,4],[5,4]], columns = ["a","b"] )
y = x.groupby( "b" )
def f(df):
  return df.iloc[0]

y.apply(f).reset_index(drop=True)
