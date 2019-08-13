import os
import pandas as pd
import numpy as np


source   = "/mnt/output/conceptos_1"
top_dest = "/mnt/output/conceptos_2_subsample"
city_col = "Cód. DANE Municipio"

if not os.path.exists(top_dest):
  os.makedirs(top_dest)

dfs = {}
cities = pd.Series()
for filename in ["funcionamiento","ingresos","inversion"]:
  dfs[filename] = pd.read_csv(
      source + "/" + filename + ".csv" )
  df = dfs[filename]
  cities = ( cities .
             append( df[city_col] ) )

cities = ( cities .
           drop_duplicates() .
           reset_index() )

for filename in ["funcionamiento","ingresos","inversion"]:
  for subsample in [1,10,100,1000]:
    sub_dest = top_dest + "/" + "recip-" + str(subsample)
    if subsample==1:
      if os.path.exists(  sub_dest ):
        os.remove(        sub_dest )
      os.symlink( source, sub_dest )
    else:
      cities_subset = pd.DataFrame(
        cities.sample(
          frac = 1/subsample,
          random_state = 0 ), # seed
        columns = [city_col] )
      if not os.path.exists( sub_dest ):
        os.makedirs(         sub_dest )
      ( dfs[filename] .
        merge( cities_subset,
               how = "inner",
               on = city_col ) .
        to_csv(
          sub_dest + "/" + filename + ".csv",
          index = False ) )

