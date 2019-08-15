# This code attempts to test against a stored reference,
# not only column types and fraction missing (as the code in production does),
# but also min and max values.
#
# It's tricky, because:
#
# (1) Columns of each type (numeric, bool, string)
# have to be treated separately in order for a "minimum over some columns"
# series to be comparable (it can't have mixed types),
# and because
#
# (2) Even if you figure out how to do that for a given data set,
# how can you keep doing it downstream without generating a new reference data set?
# And if it's a new reference data set, how can you avoid circularity in the tests?

stats_ref, stats = ({},{})
for s in ["ingresos"]:
  df = dfs[s]
  stats[s] = pd.DataFrame(
    { "dtype"   :     df.dtypes.astype( str ),
      "min"     :     df.min(),
      "max"     :     df.max(),
      "missing" : 1 - df.count() / len(df) } )
  stats_ref[s] = pd.concat(
    [ pd.read_csv( "Code/stats/raw/" + s + ".csv",
                   index_col = 0 ),
      pd.read_csv( "Code/stats/item_columns/" + s + ".csv",
                   index_col = 0 ) ] ,
    axis = "rows" )
for _ in [1]:
  stats_num     = ( stats[s] .
                    loc[ stats[s]["dtype"] .
                         isin( ["int64","float64"] ) ] )
  stats_ref_num = ( stats_ref[s] .
                    loc[ stats_ref[s]["dtype"] .
                         isin( ["int64","float64"] ) ] )
  stats_obj     = stats[s]     .loc[ stats[s]["dtype"] == "object" ]
  stats_ref_obj = stats_ref[s] .loc[ stats_ref[s]["dtype"] == "object" ]
  stats_bool     = stats[s]     .loc[ stats[s]["dtype"] == "bool" ]
  stats_ref_bool = stats_ref[s] .loc[ stats_ref[s]["dtype"] == "bool" ]
  assert ( (  stats_ref[s]["dtype"]  )
           == (stats[s]["dtype"]  ) ) . all()
  assert ( (  stats_ref_bool["min"].astype( bool ) )
           <= (stats_bool[   "min"].astype( bool ) ) ).all()
  assert ( (  stats_ref_num["min"].astype(float) )
           <= (stats_num[   "min"].astype(float) ) ).all()
  assert ( (  stats_ref_num["max"].astype(float) )
           >= (stats_num[   "max"].astype(float) ) ).all()
  assert ( (2*stats_ref[s]["missing"])
           >= (stats   [s]["missing"]) ) . all()
