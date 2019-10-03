from typing import List
import pandas as pd
import Code.metadata.raw_series as sm


group_fields = [
  "year",
  "muni code",
  "dept code",
  "item code" ]

percentiles = [0.9,
               0.99,
               0.999,
               0.9999,
               0.99999]
percentiles_str = ["50%",
                   "90%",
                   "99%",
                   "99.9%",
                   "99.99%",
                   "99.999%" ]

def how_I_calculated_non_group_fields( df : pd.DataFrame ) -> List[str]:
  """ After running this on each data set,
  I manually removed some redundant fields 
  (e.g. no "Fuente" if we already have "Codigo Fuente")."""
  def not_starts_with_item( s : str ):
    return not s[:4] == "item"
  return list(
    set.difference(
      set( filter( not_starts_with_item, drr.columns ) ),
      set( group_fields + ["muni","name","dept","one"] ) ) )

# These are not *currently* used for grouping, but could plausibly be.
# They therefore exclude possibilities like the peso-valued columns.
non_group_fields = {
  "inversion" : ['Código FUT', 'Código Fuentes De Financiación'],
  "ingresos" : [
    'Código FUT', 'Sin Situación Fondos', 'Valor Destinación',
    'Tiene Documento', 'Porción Destinanción', 'Número Documento'],
  "funcionamiento" : [ 'Código FUT', 'Código Unidad Ejecutora',
                       'Código Fuente Financiación'] }

def fetch_series( series : str ) -> pd.DataFrame:
  acc = pd.DataFrame()
  for year in range(2012,2019):
    df = (
      pd.read_csv(
        "data/sisfut/original_csv/" + str(year) + "_" + series + ".csv" ) .
      rename( columns = dict( sm.column_subsets[series] ) ) )
    df["year"] = year
    acc = acc.append( df )
  acc["one"] = 1
  return acc

def report( df : pd.DataFrame,
            more_group_fields : List[str] ) -> pd.DataFrame:
  df = (
    df . copy()
    [ group_fields + more_group_fields + ["one"] ] .
    groupby( group_fields + more_group_fields ) .
    agg( sum ) .
    reset_index() )
  return ( df["one"] .
           describe( percentiles = percentiles ) )

def report_1_extra_groupvar( df : pd.DataFrame,
                             non_group_fields : List[str]
                           ) -> pd.DataFrame:
  acc = pd.DataFrame()
  for f in non_group_fields:
    r = report(df,[f])
    r["i"] = f # The new, extra grouping column ("i" is for 'index").
    acc = acc.append( r )
  return acc

def report_2_extra_groupvars( df : pd.DataFrame,
                              non_group_fields : List[str]
                            ) -> pd.DataFrame:
  acc = pd.DataFrame()
  a = 0
  while a < len( non_group_fields ):
    b = a+1
    while b < len( non_group_fields ):
      fa = non_group_fields[a]
      fb = non_group_fields[b]
      r = report( df,
                  [fa,fb] )
      r["i1"] = fa
      r["i2"] = fb
      acc = acc.append(r)
      b += 1
    a += 1
  return acc

def report_3_extra_groupvars( df : pd.DataFrame,
                              non_group_fields : List[str]
                            ) -> pd.DataFrame:
  acc = pd.DataFrame()
  a = 0
  while a < len( non_group_fields ):
    b = a+1
    while b < len( non_group_fields ):
      c = b+1
      while c < len( non_group_fields ):
        fa = non_group_fields[a]
        fb = non_group_fields[b]
        fc = non_group_fields[c]
        r = report( df,
                    [fa,fb,fc] )
        r["i1"] = fa
        r["i2"] = fb
        r["i3"] = fc
        acc = acc.append(r)
        c += 1
      b += 1
    a += 1
  return acc

