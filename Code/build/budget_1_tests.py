import numpy  as np
import pandas as pd

import Code.metadata.three_series as sm


def row_numbers_raw( dfs ):
  """That these lengths are appropriate can be verified
  by running `wc *file*` in data/sisfut/original_csv
  and subutracting seven (which is the number of years,
  and therefore the number of header files)."""
  for (file,length) in [ ( "ingresos"      , 993934 ),
                         ( "inversion"     , 1750676 ),
                         ( "funcionamiento", 1454498 ) ]:
    assert len( dfs[file] ) == length
 
def column_names_of_raw_data( dfs ):
  for i in sm.series:
    assert ( list( dfs[i].columns ) ==
             ( sm.column_subsets_no_dups_short[i] +
               ["year"] ) )

def types_and_missings_for_raw_data( dfs ):
  stats, stats_ref = ({},{})
  for s in ["ingresos"]:
    df = dfs[s]
    stats[s] = pd.DataFrame(
      { "dtype"   :     df.dtypes.astype( str ),
#       "min"     :     df.min(), # TODO : use, somehow
#       "max"     :     df.max(), # TODO : use, somehow
        "missing" : 1 - df.count() / len(df) } )
    stats_ref[s] = pd.read_csv( "Code/integ_tests/raw/" + s + ".csv",
                                index_col = 0 )
    assert stats_ref[s]["dtype"]   . equals( stats[s]["dtype"]  )
    assert stats_ref[s]["missing"] . equals( stats[s]["missing"])

