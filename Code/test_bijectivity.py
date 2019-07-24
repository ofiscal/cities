# Determine whether the columns in each duplicative pair
# (defined in Code.sisfut_about) indeed correspond 1-to-1.

from itertools import chain
import pandas as pd
import Code.sisfut_about as sc

dup_columns = pd.DataFrame()
for series in ["ingresos","inversion","funcionamiento"]:
  for year in range( 2012, 2018+1 ):
    shuttle = pd.read_csv(
      ( sc.source_folder + "original_csv/"
        + str(year) + "_" + series + ".csv" )
      , usecols = set.intersection(
          set( sc.column_subsets[series] )
        , sc.duplicative_columns_set )
    )
  dup_columns = dup_columns.append( shuttle )

# "duplicate pairs": each frame below has 2 columns
dps, dps_unique_pairs, dps_counts = ({},{},{})
for p in sc.duplicative_columns:
  dps[p] = dup_columns[[ p[0], p[1] ]].copy()
  dps[p]["dummy"] = 0
    # so that |rows| > 0 after .agg() step
  dps_unique_pairs[p] = dps[p].groupby(list(p)).agg(max)
  dps_unique_pairs[p]["unit"] = 1
  dps_unique_pairs[p] = dps_unique_pairs[p].drop(columns="dummy")
  for i in [0,1]:
    dps_counts[p[i]] = (
      dps_unique_pairs[p].groupby( p[i] ).agg(sum)
      )
    print(p[i])
    print( dps_counts[p[i]].describe() )

# TODO: complete
# Demo: How to find many-to-one mappings
x = ( dps_counts["Nombre DANE Municipio"]
      . reset_index() )
y = ( dps_unique_pairs[("Cód. DANE Municipio", "Nombre DANE Municipio")]
      . reset_index() )
x0 = x[ x["unit"] > 1 ]
y.merge(x0, on="Nombre DANE Municipio")
