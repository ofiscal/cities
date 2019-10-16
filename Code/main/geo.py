# This creates the list of municipalities to process.
# It depends on the sample size.

if True:
  import pandas as pd
  import Code.common as c
  import Code.build.use_keys as uk

if True: # create geo indices to loop over
  geo = uk.merge_geo( # Using stage 6p7 rather than 7 because
    pd.read_csv(      # they are equivalent and it's smaller
      ( "output/budget_6p7_avg_muni/recip-" + str(c.subsample) +
        "/" + "gastos-pct.csv" ),
      usecols = ['dept code', 'muni code'] ) .
    drop_duplicates() .
    reset_index( drop=True ) .
    sort_values( ["dept code","muni code"] ) )
  geo = geo[ geo["muni code"] > 0 ]

