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

dup_pairs, dup_pairs_agg, dup_pairs_agg_max = ({},{},{})
for p in sc.duplicative_columns:
  dup_pairs[p] = dup_columns[[ p[0], p[1] ]].copy()
  dup_pairs[p]["count"] = 1
  # TODO: Add the count=1 variable *after* aggregating.
  # It's uninteresting how many times a dup pair occurs before then.
  # What's interesting is whether any value in either of those pairs
  # occurs more than once after aggregating on both of them.
  # That will require a second aggregation.
  dup_pairs_agg[p] = dup_pairs[p].groupby( p )
  dup_pairs_agg_max[p] = dup_pairs_agg[p].agg(max)
  print( dup_pairs_agg_max[p].describe() )
