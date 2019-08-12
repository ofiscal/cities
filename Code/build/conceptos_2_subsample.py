import os
import pandas as pd
import numpy as np


source   = "/mnt/output/conceptos_1"
top_dest = "/mnt/output/conceptos_2_subsample"

if not os.path.exists(top_dest):
  os.makedirs(top_dest)

dfs = {}
for filename in ["funcionamiento","ingresos","inversion"]:
  dfs[filename] = pd.read_csv(
      source + "/" + filename + ".csv" )

for filename in ["funcionamiento","ingresos","inversion"]:
  df = dfs[filename]
  for subsample in [1,10,100,1000]:
    sub_dest = top_dest + "/" + "recip-" + str(subsample)
    if subsample==1:
      if os.path.exists(  sub_dest ):
        os.remove(        sub_dest )
      os.symlink( source, sub_dest )
    else:
      if not os.path.exists(sub_dest):
        os.makedirs(        sub_dest)
      ( df.sample( frac = 1/subsample,
                   random_state = 0 ) . # seed
        to_csv( sub_dest + "/" + filename + ".csv" ) )
