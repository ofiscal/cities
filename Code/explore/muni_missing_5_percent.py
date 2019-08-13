# Demonstrates that 3% to 5% of observations in each data set
# are missing both municipality (name) and municipality code.
 itertools import chain
import numpy as np
import pandas as pd
import Code.build.aggregation_regexes as ac
import Code.build.sisfut_metadata as sm


def get_raw_data():
  dfs = {}
  for series in sm.series:
    dfs[series] = pd.DataFrame()
    for year in range( 2012, 2018+1 ):
      shuttle = (
        pd.read_csv(
          ( sm.source_folder + "original_csv/"
            + str(year) + "_" + series + ".csv" )
  #        , nrows = 20000
          , usecols = [ "Cód. DANE Municipio",
                        "Nombre DANE Municipio" ] ) .
        rename( columns = dict( sm.column_subsets[series] ) ) )
      shuttle["year"] = year
      dfs[series] = dfs[series] . append(shuttle)
  return dfs

def get_output_data(folder):
  dfs = {}
  for series in sm.series:
    dfs[series] = pd.read_csv( folder + "/" + series + ".csv" )
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

dfs = get_raw_data()
analyze( dfs )

dfs1 = get_output_data("output/conceptos_1")
analyze( dfs1 )

dfs2 = get_output_data("output/conceptos_2/recip-1")
analyze( dfs )

