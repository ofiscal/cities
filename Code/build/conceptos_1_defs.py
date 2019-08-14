import numpy as np
import pandas as pd
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


def collect_raw(nrows = None):
  """Returns a dictionary of three data frames, one for each of ingresos, inversion and funcionamiento. If using the optional 'nrows' argument, bear in mind that the 3 data sets have about 4 million rows between them."""
  dfs = {}
  for series in sm.series:
    dfs[series] = pd.DataFrame()
    for year in range( 2012, 2018+1 ):
      shuttle = (
        pd.read_csv(
          ( sm.source_folder + "original_csv/"
            + str(year) + "_" + series + ".csv" )
          , nrows = nrows
          , usecols = set.difference(
              set( sm.column_subsets_long[series] )
            , sm.omittable_columns_long ) ) . # omit the omittable ones
        rename( columns = dict( sm.column_subsets[series] ) ) )
      shuttle["year"] = year
      dfs[series] = dfs[series] . append(shuttle)
  return dfs


######
###### Build aggregated concepto-code columns.
######
# 

def aggregated_item_codes( dfs ):
  """An 'item' is a record of spending or income (taxes). This function builds some new columns, the aggregate item subcodes by which the data will downstream be aggregated. It does not aggregate rows. The 'dfs' argument should be a dictionary containing the three data sets, per collect_raw()."""
  for (series, regexes) in [
        ("inversion"      , ac.regexes_for_2_codes() )
      , ("funcionamiento" , ac.regexes_for_2_codes() )
      , ("ingresos"       , ac.regexes_for_ingresos() ) ]:
    df = dfs[series]
  
    # build some columns
    (category, top, child) = regexes
    df["item categ"]       = (
        df["item code"]
      . str.extract( category ) )
    df["item top"]   = ~ pd.isnull(
        df["item code"]
      . str.extract( top ) )
    df["item child"] = ~ pd.isnull(
        df["item code"]
      . str.extract( child ) )
  
    df = ( # keep only rows labeled with top categories
           # or the first generation below the top categories
      df[ (df["item top"])
        | (df["item child"]) ] )
  
    # Verify that codigo-top is the boolean negative of codigo-child.
    # (That's not true before we drop rows categorized deeper than top or child.)
    assert ( len ( df[ ( (df["item top"].astype(int)) +
                         (df["item child"]).astype(int) )
                       != 1 ] )
             == 0 )
    df = df.drop( columns = ["item child"] )
  
    dfs[series] = df
  return dfs
