# The pivot tables from the previous stage describe
# how a place's finances have evolved over time.
# These tables will compare how their sum over the last
# three years to that of the department average.

if True:
  from typing import List,Set,Dict
  import os
  from pathlib import Path
  import pandas as pd
  #
  import Code.common as c
  import Code.util.aggregate_all_but_biggest.better \
    as agger # "aggregator"
  import Code.metadata.four_series as s4

if True:
  grouped_root = "output/pivots/recip-" + str(c.subsample)
  spacetime = ["dept", "muni", "year", "dept code", "muni code"]
  space     = ["dept", "muni",         "dept code", "muni code"]

if True: # read a few big tables
  ungrouped : Dict[str, pd.DataFrame] = {}
  for s in s4.series:
    ungrouped[s.name] = (
      pd.read_csv(
        ( "output/budget_7_verbose/recip-" + str(c.subsample)
          + "/" + s.name + ".csv") ) .
      sort_values( spacetime ) )

if True: # build geo indices of interest
  geo = ungrouped[s.name] . copy()
  geo = ( geo[space] .
         groupby( space ) .
         agg( 'first' ) .
         reset_index() )

def static_muni( filename : str,
                 dept_code : int,
                 muni_code : int
               ) -> pd.DataFrame:
  d = str( geo.loc[ geo["muni code"]==muni_code,
                    "dept" ] .
           iloc[0] )
  m = ( str( geo.loc[ geo["muni code"]==muni_code,
                      "muni" ] .
             iloc[0] )
        if muni_code > 0
        else "promedio" )
  df = pd.read_csv(
    ( grouped_root + "/" + d + "/" + m +
      "/" + filename + ".csv" ),
    index_col="item categ" )
  df.columns = list( map( int,
                          map( float, df.columns ) ) )
  return ( df[[2016,2017,2018]] .
           sum( axis="columns" ) )

def static_avg_with_otros(
    filename : str,
    dept_code : int,
    sm : pd.DataFrame # result of calling static_muni()
    ) -> pd.DataFrame:
  """ Only needed for gastos data sets."""
  top_rows = sm.index.drop( "Otros" )
  df = static_muni( filename, dept_code, -2 )
  df_top = df.loc[top_rows]
  df_bottom = pd.Series( [ df . copy() .
                           drop( index = top_rows ) .
                           sum() ],
                         index = ["Otros"] )
  return ( pd.concat( [df_top,df_bottom] ) .
           loc[df.index] ) # reorder

