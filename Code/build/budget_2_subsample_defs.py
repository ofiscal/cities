import os
import pandas as pd
import numpy as np

import Code.build.sisfut_metadata as sm


source   = "/mnt/output/budget_1p5"
top_dest = "/mnt/output/budget_2_subsample"
  # destinations are immediate child folders of this folder

def sub_dest( subsample ):
  return top_dest + "/" + "recip-" + str( subsample )

def read_data( nrows = None ):
  """Returns a dictionary of three data frames."""
  dfs = {}
  for filename in ["ingresos","gastos"]:
    df = pd.read_csv( source + "/" + filename + ".csv",
                      encoding = "utf-16",
                      nrows = nrows )
    dfs[filename] = df
  return dfs

def munis_unique_without_nan( dfs ):
  """Creates a pandas DataFrame that contains every "muni code" value exactly ones, given a dictionary of three data frames."""
  munis = pd.DataFrame()
  for s in ["ingresos","gastos"]:
    munis = pd.concat( [ munis,
                         dfs[s] ["muni code"] ],
                       axis = "rows" )
  munis.columns = ["muni code"]
  munis = munis[
    ~ pd.isnull(
      munis["muni code"] ) ]
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
  for filename in ["ingresos","gastos"]:
    dfs2[filename] = (
      dfs2[filename] .
      merge( munis_subset,
             how = "inner",
             on = "muni code" ) )
  return dfs2
