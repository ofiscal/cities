# Determine whether the columns in each duplicative pair
# (defined in Code.sisfut_about) indeed correspond 1-to-1.
# They mostly are.
# Anomalies are written to output/non_bijective/.

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
  dps_unique_pairs[p]["count"] = 1
  dps_unique_pairs[p] = dps_unique_pairs[p].drop(columns="dummy")
  for i in [0,1]:
    dps_counts[p[i]] = (
      dps_unique_pairs[p]
      . groupby( p[i] )
      . agg(sum) )

problems = {}
for p in sc.duplicative_columns:
  for i in (0,1):
    if dps_counts[p[i]]["count"].max() > 1:
      print( p, i )
      x = ( dps_counts[p[i]]
            . reset_index() )
      y = ( dps_unique_pairs[p]
            . reset_index()
            . drop( columns = "count" ) )
      x0 = x[ x["count"] > 1 ]
      problems[p[i]] = y.merge(x0, on=p[i])
      problems[p[i]].to_csv( "output/non_bijective/" +
                             p[i] + ".csv"
                           , index = False )
