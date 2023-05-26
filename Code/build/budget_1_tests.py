if True:
  from typing import Dict,Set,List
  import numpy  as np
  import pandas as pd
  #
  from   ofiscal_utils.math import near
  from   Code.common import vintage
  import Code.metadata.terms as t
  import Code.metadata.raw_series as sm


# TODO: This would be more elegant if it ran `wc *x*` on the data
# (where x takes values in "ingresos", "funcionamiento", etc.)
# and subtracted (last year - first year) from the result.
def row_numbers_raw( dfs ):
  """That these lengths are appropriate can be verified
  by running `wc *file*` in data/sisfut/csv
  and subutracting seven (which is the number of years,
  and therefore the number of header lines)."""
  for (file,length) in (
      [ ( t.ingresos      , 862530  ),
        ( t.inversion     , 1525111 ),
        ( t.funcionamiento, 1258049 ),
        ( t.deuda         , 44864   ) ]
      if vintage == 2019
      else
      [ ( t.ingresos      , 1187152 - 9 ),
        ( t.inversion     , 2117275 - 9 ),
        ( t.funcionamiento, 1730814 - 9 ) ] ):
    # TODO ? This would have to be equality, not near-equality,
    # except that CSV files can contain newlines in a row,
    # assuming it is wrapped in double-quotes.
    # I haven't searched for what the offending data is,
    # and it's conceivable that that's not actually the reason
    # these aren't always exactly equal.
    x = len( dfs[file] )
    assert near ( x, length )
    if x != length:
      print ( "WARNING: ", file, " has length ", length,
              " but data has length ", x )

def column_names_of_raw_data( dfs ):
  for i in sm.series:
    assert ( list( dfs[i].columns ) ==
             ( sm.column_subsets_no_dups_short[i] +
               ["year"] ) )

def types_and_missings_for_raw_data(
    dfs : Dict[str,pd.DataFrame] ):
  stats, stats_ref = {},{}
  for s in sm.series:
    df = dfs[s]
    stats[s] = pd.DataFrame(
      { "dtype"   :     df.dtypes.astype( str ),
      # "min"     :     df.min(), # TODO : use, somehow
      # "max"     :     df.max(), # TODO : use, somehow
        "missing" : 1 - df.count() / len(df) } )
    stats_ref[s] = pd.read_csv( "Code/integ_tests/raw/" + s + ".csv",
                                index_col = 0 )
    assert stats[s]["dtype"] . equals(
      stats_ref[s]["dtype"] )
    assert (stats[s]["missing"] <= 0.05) . all()
    assert ( ( ( stats[s].drop( index="muni code" )
                 ["missing"] )
               <= ( 1e-3 if s == t.ingresos
                    else 1e-5 ) ) .
             all() )
