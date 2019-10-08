if True:
  from typing import Dict,Set,List
  import os
  import pandas as pd
  import numpy as np
  #
  import Code.metadata.terms as t
  import Code.metadata.raw_series as sm


if True: # bearings
  # These folders must be absolute, not relative,
  # in order for the recip-1 symlink to work
  source   = "/mnt/output/budget_1p5"
  top_dest = "/mnt/output/budget_2_subsample"
    # destinations are immediate child folders of this folder
  def sub_dest( subsample ):
    return top_dest + "/" + "recip-" + str( subsample )

def read_data( nrows = None ):
  """Returns a dictionary of three data frames."""
  dfs = {}
  for filename in [t.ingresos,t.gastos]:
    df = pd.read_csv( source + "/" + filename + ".csv",
                      nrows = nrows )
    dfs[filename] = df
  return dfs

def munis_unique_no_dept( dfs : Dict[str, pd.DataFrame]
                        ) -> pd.DataFrame:
  """Creates a pandas DataFrame that contains every "muni code" value exactly once, omitting 0 (because 0 represents a dept, not a muni)."""
  munis = pd.DataFrame()
  for s in [t.ingresos,t.gastos]:
    munis = pd.concat( [ munis,
                         dfs[s] ["muni code"] ],
                       axis = "rows" )
  munis.columns = ["muni code"]
  munis = munis[ munis["muni code"] != 0 ] # drop dept-level observations
  return ( munis .
           drop_duplicates() )

def subsample( subsample : int,
               df : pd.DataFrame ) -> pd.DataFrame:
  return df.sample( frac = 1/subsample,
                    random_state = 0 ) # seed

def dfs_subset( munis_subset, dfs ):
  dfs2 = {}
  for s in dfs.keys(): # deep copy
    dfs2[s] = dfs[s].copy()
  for filename in [t.ingresos,t.gastos]:
    df = dfs2[filename]
    df = df[ df["muni code"] .
             isin( set(
               munis_subset["muni code"] ) ) ]
    dfs2[filename] = df
  return dfs2

