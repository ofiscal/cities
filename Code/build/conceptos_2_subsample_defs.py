import os
import pandas as pd
import numpy as np

import Code.build.sisfut_metadata as sm


source   = "/mnt/output/conceptos_1"
top_dest = "/mnt/output/conceptos_2_subsample"
  # destinations are immediate child folders of this folder

def sub_dest( subsample ):
  return top_dest + "/" + "recip-" + str( subsample )

def read_data():
  """Returns a dictionary of three data frames."""
  dfs = {}
  for filename in sm.series:
    dfs[filename] = pd.read_csv(
        source + "/" + filename + ".csv" )
  return dfs

def munis_unique( dfs ):
  """Creates a pandas Series that contains every "muni code" value exactly ones, given a dictionary of three data frames."""
  munis = pd.Series()
  for s in sm.series:
    munis = ( munis .
              append( dfs[s]
                      ["muni code"] ) )
  return ( munis .
           drop_duplicates() .
           reset_index() )

def munis_subset( subsample : int, munis : pd.Series ) -> pd.DataFrame:
  return pd.DataFrame(
    munis.sample(
      frac = 1/subsample,
      random_state = 0 ), # seed
    columns = ["muni code"] )

def dfs_subset( munis_subset, dfs ):
  dfs2 = dfs.copy()
  for filename in sm.series:
    dfs2[filename] = (
      dfs2[filename] .
      merge( munis_subset,
             how = "inner",
             on = "muni code" ) )
  return dfs2
