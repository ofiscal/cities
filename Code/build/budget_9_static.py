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
  import Code.metadata.terms as t
  import Code.metadata.four_series as s4

testing = True

if True:
  monolith_root = "output/budget_7_verbose/recip-" + str(c.subsample)
  by_place_root = "output/pivots/recip-"           + str(c.subsample)
  spacetime = ["dept", "muni", "year", "dept code", "muni code"]
  space     = ["dept", "muni",         "dept code", "muni code"]

if True: # read a few big tables
  monolith : Dict[str, pd.DataFrame] = {}
  for s in s4.series_pct:
    monolith[s.name] = ( # These data sets are "monolithic" in that
      # all munis are contained together in the same data set.
      # By contrast, each output of this file corresponds to
      # to a separate muni.
      pd.read_csv( monolith_root + "/" + s.name + ".csv") .
      sort_values( spacetime ) )

geo = ( # geo indices of interest
  monolith[ t.ingresos_pct] .
    # smaller than, and (here) equivalent to, t.gastos_pct
  copy()
  [space] .
  drop_duplicates() )

def static_muni( filename : str,
                 dept_code : int,
                 muni_code : int
               ) -> pd.Series:
  assert muni_code > 0
  d = str( geo.loc[ geo["muni code"]==muni_code,
                    "dept" ] .
           iloc[0] )
  m = str( geo.loc[ geo["muni code"]==muni_code,
                    "muni" ] .
           iloc[0] )
  fn = ( by_place_root + "/" + d + "/" + m +
         "/" + filename + ".csv" )
  df = pd.read_csv( fn,
    index_col="item categ" )
  df.columns = list( map( int,
                          map( float, df.columns ) ) )
  return ( df[[2016,2017,2018]] .
           sum( axis="columns" ) )

if testing: # Test by hand
  static_muni( "gastos-pct", 25, 25873 )

def static_avg( filename : str,
                money_col : str,
                dept_code : int,
              ) -> pd.Series:
  df = monolith[filename] . copy()
  df = df [ (df["dept code"]==dept_code) &
            (df["muni code"] > 0) & # exclude dept-level info
            (df["year"] >= 2016) ]
  ms = df["munis in dept"].iloc[0]
  df = df.drop( columns = "munis in dept" )
  dg = ( df .
         groupby( ["dept code","dept","item categ"] ) .
         agg( 'sum' ) .
         reset_index() )
  res = ( dg[ money_col ] /
          float(3 * ms) ) # three because there are three years
  res.index = dg["item categ"]
  return res

if testing:
  ( static_avg( "gastos-pct", "item oblig", 25 ) .
    drop( columns = ["dept code","dept"] ) )

def static_avg_with_otros(
    filename : str,
    money_col : str,
    dept_code : int,
    sm : pd.DataFrame # result of calling static_muni()
    ) -> pd.Series:
  """ Only needed for gastos data sets."""
  top_rows = sm.index.drop( "Otros" )
  avg = static_avg( filename, money_col, dept_code )
  avg_top = avg.loc[top_rows]
  avg_bottom = ( pd.Series( [ avg . copy() .
                              drop( index = top_rows ) .
                              sum() ],
                            index = ["Otros"] ) .
                 fillna(0) )
  return ( pd.concat( [avg_top,avg_bottom] ) )
#           loc[avg.index] )

if testing: # Test by hand
  static_avg_with_otros(
    "gastos-pct",
    "item oblig",
    25,
    static_muni( "gastos-pct", 25, 25873 ) )

def static_muni_pair(
    filename : str,
    money_col : str,
    dept_code : int,
    muni_code : int,
    ) -> pd.DataFrame:
  m = static_muni(
    filename, dept_code, muni_code )
  m_name = str( geo[geo["muni code"]==muni_code]["muni"].iloc[0] )
  d_name = str( geo[geo["muni code"]==muni_code]["dept"].iloc[0] )
  a = ( ( static_avg_with_otros(
            filename, money_col, dept_code, m ) )
        if filename == "gastos-pct"
        else static_avg(
            filename, money_col, dept_code ) )
  return pd.DataFrame(
    { m_name                  : m,
      "promedio en " + d_name : a } )

if testing:
  static_muni_pair( "gastos-pct", "item oblig", 25, 25873 )
  static_muni_pair( "ingresos-pct", "item total", 25, 25873 )

for s in s4.series_pct:
  ( geo[geo["muni code"] > 0] .
      # exclude rows about depts or average munis
    apply(
      ( lambda row:
        static_muni_pair( s.name,
                          s.money_cols[0],
                          row["dept code"],
                          row["muni code"] ) .
        to_csv( by_place_root + "/" + row["dept"] + "/" +
                row["muni"] + "/" + s.name + "-compare.csv" ) ),
      axis = "columns" ) )


