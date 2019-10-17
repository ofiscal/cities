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
  import Code.util.fill_subspace as fill

testing = True if c.subsample == 100 else False

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

def static_muni_ungrouped( filename : str,
                           dept_code : int,
                           muni_code : int
                         ) -> pd.Series:
  """Average a muni's values over years after 2015."""
  assert muni_code > 0
  money_col = ( "item total"
                if filename == t.ingresos_pct
                else "item oblig" )
  d = str( geo.loc[ geo["muni code"]==muni_code,
                    "dept" ] .
           iloc[0] )
  m = str( geo.loc[ geo["muni code"]==muni_code,
                    "muni" ] .
           iloc[0] )
  df = monolith[filename]
  df = ( df[ (df["dept code"]==dept_code) &
             (df["muni code"]==muni_code) &
             (df["year"] > 2015) ]
         [[ "year", "item categ",money_col ]] .
         copy() )
  df = fill.fill_space( ["year","item categ"],
                        [money_col],
                        df )
  df = ( df[["item categ",money_col]] .
         groupby( ["item categ"] ) .
         agg( 'mean' )
         [money_col] .
         sort_values() )
  return df

if testing:
  dc, mc = 25, 25873 # Villapinzón, in Cundinamarca
  fn = "gastos-pct"
  df = monolith[fn]
  df = df[ (df["dept code"]==dc) &
           (df["muni code"]==mc) &
           (df["year"] > 2015) ]
  (df . groupby( "item categ" ) . agg("mean") )["item oblig"]
  static_muni_ungrouped( fn, dc, mc )

def group_small_if_needed( filename : str,
                           ser : pd.Series
                         ) -> pd.Series:
  if filename == "ingresos-pct":
    return ser
  else: # lump all but the top five gastos
        # together under "Otros"
    ser = ser.sort_values( ascending = False )
    ser_top       = ser . iloc[0:5]
    ser_new_otros = pd.Series(
        ser . iloc[5:] . sum() )
    ser_new_otros.index = ["Otros"]
    return pd.concat( [ser_top, ser_new_otros] )

def static_muni( filename : str,
                 dept_code : int,
                 muni_code : int
               ) -> pd.Series:
  return group_small_if_needed(
    filename,
    static_muni_ungrouped( filename,
                           dept_code,
                           muni_code ) )

if testing: # Test by hand
  filename = "gastos-pct"
  dc = 25
  mc = 25873
  d = monolith[filename]
  d = ( d[ ( d["dept code"] == dc) &
           ( d["muni code"] == mc) &
           ( d["year"]      >= 2016 ) ] )
  d = ( d . drop( columns = ["dept","muni"] ) .
        rename(
          columns = {"munis in dept":"ms",
                     "muni-years in dept" : "mys" } ) )
  d = ( d[ ( d["item categ"] == "Salud" ) ] .
        copy() )
  d["item categ"] = ( d["item categ"] .
                      apply( lambda s: s[:10] ) )
  d
  d["item oblig"].mean()
  static_muni_ungrouped( filename, 25, mc )
  static_muni( filename, 25, mc )

def static_avg( filename : str,
                money_col : str,
                dept_code : int,
              ) -> pd.Series:
  df = monolith[filename]
  df = df [ (df["dept code"]==dept_code) &
            (df["muni code"] > 0) & # exclude dept-level info
            (df["year"] >= 2016) ] . copy()
  muni_years = df["muni-years in dept"].iloc[0]
    # .iloc[0] is fine, becaused |muni-years| is constant in df
  dg = ( df[["item categ",money_col]] .
         groupby( "item categ" ) .
         agg( 'sum' ) .
         reset_index() )
  res = dg[ money_col ] / muni_years
  res.index = dg["item categ"]
  return res

if testing: # PITFALL: Theese numbers cannot simply be read off
  # the time-series charts; they require averaging  the last three years
  # for every muni in the dept, and then averaging those.
  dc = 19
  filename = "gastos-pct"
  money_col = "item oblig"
  df = monolith[filename]
  df = df [ (df["dept code"]==dc) &
            (df["muni code"] > 0) & # exclude dept-level info
            (df["year"] >= 2016) ] . copy()
  df[["dept","muni","year","item categ"]]
  #
  df_readable = df.copy()
  df_readable["item categ"] = df["item categ"] . apply(
    lambda s: s[:10] )
  df_readable.drop( columns = ["dept","muni"] )
  df_readable.drop( columns = ["dept","muni",
                               "munis in dept","muni-years in dept"] )
  #
  df.describe().transpose()
  muni_years = df["muni-years in dept"].iloc[0]
  #
  df = df[["item categ",money_col]]
  test = ( ( ( df .
               groupby( "item categ" ) .
               agg( 'sum' ) ) /
             muni_years )
           [money_col] )
  func = ( static_avg( filename, money_col, dc ) .
           drop( columns = ["dept code","dept"] ) )
  res = pd.concat( [test,func],
                   axis = "columns" )
  res.columns = ["test","func"]
  res

def static_avg_with_otros(
    filename : str,
    money_col : str,
    dept_code : int,
    sm : pd.DataFrame # result of calling static_muni()
    ) -> pd.Series:
  """ Like `static_avg()`, but lumps together every row not in the `sm` argument. Only for gastos data sets only."""
  top_rows = sm.index.drop( "Otros" )
  avg = static_avg( filename, money_col, dept_code )
  avg_top = avg.loc[top_rows]
  avg_bottom = ( pd.Series( [ avg . copy() .
                              drop( index = top_rows ) .
                              sum() ],
                            index = ["Otros"] ) .
                 fillna(0) )
  return pd.concat( [avg_top, avg_bottom] )

if testing: # Test by hand
  dc = 25
  mc = 25873
  sm = static_muni( "gastos-pct", dc, mc )
  sa = static_avg( "gastos-pct",
                   "item oblig",
                   dc )
  sawo = static_avg_with_otros( "gastos-pct",
                                "item oblig",
                                dc,
                                sm )
  res = pd.concat( [sm,sa,sawo],
                   axis = "columns",
                   sort = True )
  res.columns = ["sa","sm","sawo"]
  res

def static_muni_pair( filename : str,
                      money_col : str,
                      dept_code : int,
                      muni_code : int
                    ) -> pd.DataFrame:
  m = static_muni(
    filename, dept_code, muni_code )
  m_name = str( geo[geo["muni code"]==muni_code]
                ["muni"].iloc[0] )
  d_name = str( geo[geo["muni code"]==muni_code]
                ["dept"].iloc[0] )
  print( str(dept_code), d_name, str(muni_code), m_name, filename )
  a = ( static_avg_with_otros(
          filename, money_col, dept_code, m )
        if filename == "gastos-pct"
        else static_avg(
               filename, money_col, dept_code ) )
  return pd.DataFrame(
    { m_name                  : m,
      "promedio en " + d_name : a } )

if testing:
  ing = static_muni_pair( "ingresos-pct", "item total", 25, 25873 )
  ing.index = map( lambda s: s[:20], ing.index )
  ing
  static_muni_pair( "gastos-pct", "item oblig", 25, 25873 )

def series_to_frame( ser : pd.Series ) -> pd.DataFrame:
  df = pd.DataFrame( ser )
  df.columns = ["promedio 2016-2018"]
  return df

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

  if s.name == t.gastos_pct:
    ( geo[geo["muni code"] > 0] .
        # exclude rows about depts or average munis
      apply(
        ( lambda row:
          series_to_frame(
            static_muni_ungrouped( s.name,
                                   row["dept code"],
                                   row["muni code"] ) ) .
          to_csv( by_place_root + "/" + row["dept"] + "/" +
                  row["muni"] + "/" + s.name + "-ungrouped.csv" ) ),
        axis = "columns" ) )

( Path( by_place_root + "/" + "timestamp-for-static-compare" ) .
  touch() )

