# Demonstrates that 3% to 5% of observations in each data set
# are missing both municipality (name) and municipality code.

#Examples of how to use this code.
#dfs = get_raw_data()
#analyze( dfs )
#
#dfs1 = get_output_data("output/budget_1")
#analyze( dfs1 )
#
#dfs2 = get_output_data("output/budget_2/recip-1")
#analyze( dfs )

import os.path as path
import numpy as np
import pandas as pd
#
import Code.build.aggregation_regexes as ac
import Code.metadata.raw_series as sm
import Code.common as common


def get_raw_data():
  dfs = {}
  for series in sm.series:
    dfs[series] = pd.DataFrame()
    for year in range( 2012, 2018+1 ):
      shuttle = (
        pd.read_csv (
          path.join ( "data", str(common.vintage), "sisfut", "csv",
                      str(year) + "_" + series + ".csv" ),
          # nrows = 20000
          usecols = [ "Cód. DANE Municipio",
                      "Nombre DANE Municipio" ] ) .
        rename( columns = dict( sm.column_subsets[series] ) ) )
      shuttle["year"] = year
      dfs[series] = dfs[series] . append(shuttle)
  return dfs

def get_output_data(folder):
  dfs = {}
  for series in sm.series:
    dfs[series] = pd.read_csv (
      path.join ( folder,
                  series + ".csv" ) )
  return dfs

def analyze( dfs ):
  for s in sm.series:
    print(s)
    df = dfs[s]
    df_bad = df[
      ( df["muni code"] .isnull() ) |
      ( True if not "muni" in df.columns
        else df["muni"]      .isnull() ) ]
    print( len(df_bad) / len(df) )
