###### ABOUT THE NAME
###### 1p5 means "1.5". That is, this program runs after budget_1
###### and before budget_2.
###### (I can't include a dot in the name without confusing Python.)

###### PURPOSE
###### This restricts the data to the budget items of interest,
###### as specified by `of interest`, which is defined in
###### `Code.build.classify_budget_codes`.
###### It outputs only two data sets, "ingresos" and "gastos",
###### collapsing three of the four inputs data sets into "gastos".

if True:
  import os
  import pandas as pd
  #
  import Code.build.budget_1p5_tests as tests
  import Code.build.classify_budget_codes as cla
  import Code.metadata.terms as t
  import Code.metadata.raw_series as sm


if True: # folders
  source = "output/budget_1"
  dest = "output/budget_1p5"
  if not os.path.exists( dest ):
    os.makedirs( dest )

if True: # input data
  dfs = {}
  for s in sm.series:
    dfs[s] = pd.read_csv (
      os.path.join ( source,
                     s + ".csv" ) )

if True: # Filter rows by item code.
  dfs_filt = {}
  for s in sm.series:
    df = dfs[s]
    dfs_filt[s] = df[
      df["item code"] .
      apply( lambda c :
             c in cla.of_interest[s] ) ]

if True : # Test the result.
  for s in sm.series: # Each data set shrank, and not too much.
    assert len( dfs[s] ) > 1.5 * len( dfs_filt[s] )
    assert len( dfs[s] ) < 50 * len( dfs_filt[s] )
  tests.column_names_after_agg( sm.series, dfs_filt )

if True: # output two data sets, not four
  df_gastos = pd.concat(
    [ dfs_filt[t.funcionamiento],
      dfs_filt[t.inversion],
      dfs_filt[t.deuda] ],
    axis = "rows" )
  for (name,df) in [
        (t.ingresos, dfs_filt[t.ingresos] ),
        (t.gastos,   df_gastos) ]:
    df.to_csv( dest + "/" + name + ".csv",
               index = False )
