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

def subsample( subsample : int,
               df : pd.DataFrame ) -> pd.DataFrame:
  return df.sample( frac = 1/subsample,
                    random_state = 0 ) # seed

