if True:
  import numpy as np
  import os
  import pandas as pd
  from   typing import Dict,Set,List
  #
  import Code.common as common
  import Code.metadata.raw_series as sm
  import Code.metadata.terms as t


if True: # bearings
  home     = "/mnt"
  source   = os.path.join ( common.outdata, "budget_1p5" )
  top_dest = os.path.join ( common.outdata, "budget_2_subsample" )
    # Destinations are immediate child folders of this folder.
  def sub_dest( subsample ):
    return os.path.join ( top_dest,
                          "recip-" + str( subsample ) )

def read_data ( nrows = None ):
  """Returns a dictionary of three data frames."""
  dfs = {}
  for filename in [t.ingresos,t.gastos]:
    df = pd.read_csv (
      os.path.join ( source,
                     filename + ".csv" ),
      nrows = nrows )
    dfs[filename] = df
  return dfs

def subsample( subsample : int,
               df : pd.DataFrame ) -> pd.DataFrame:
  return df.sample( frac = 1/subsample,
                    random_state = 0 ) # seed
