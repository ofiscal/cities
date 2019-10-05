if True:
  from typing import Dict,Set,List
  import numpy  as np
  import pandas as pd
  #
  import Code.metadata.terms as t
  import Code.metadata.raw_series as sm


def row_numbers_raw( dfs ):
  """That these lengths are appropriate can be verified
  by running `wc *file*` in data/sisfut/csv
  and subutracting seven (which is the number of years,
  and therefore the number of header files)."""
  for (file,length) in [ ( t.ingresos      , 862530  ),
                         ( t.inversion     , 1525111 ),
                         ( t.funcionamiento, 1258049 ),
                         ( t.deuda         , 44864   ) ]:
    assert len( dfs[file] ) == length

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

