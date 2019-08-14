import numpy  as np
import pandas as pd

import Code.build.sisfut_metadata as sm


def row_numbers( dfs ):
  """That these lengths are appropriate can be verified
  by running `wc *file*` in data/sisfut/original_csv
  and subutracting seven (which is the number of years,
  and therefore the number of header files)."""
  for (file,length) in [ ( "ingresos", 993934 ),
                         ( "inversion", 1750676 ),
                         ( "funcionamiento", 1454498 ) ]:
    assert len( dfs[file] ) == length
  
def column_names_of_raw_data( dfs ):
  for i in sm.series:
    assert ( list( dfs[i].columns ) ==
             ( sm.column_subsets_no_dups_short[i] +
               ["year"] ) )

def column_names_after_agg( dfs ):
  for i in sm.series:
    assert ( list( dfs[i].columns ) ==
             ( sm.column_subsets_no_dups_short[i] +
               ["year", "item categ", "item top"] ) )

