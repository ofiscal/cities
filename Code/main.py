import os
import pandas as pd
import matplotlib.pyplot as plt
from   matplotlib.backends.backend_pdf import PdfPages

import Code.common as c
import Code.metadata.two_series as ser
import Code.draw.lib as lib


source = "output/budget_7_verbose/recip-" + str(c.subsample)

dfs = {}
for s in ser.series:
  df = pd.read_csv( source + "/" + s.name + ".csv" )
  dfs[s.name] = df

for s in ser.series:
  print( s.name, s.pesos_col )
  for muni in [15183]:
    df = dfs[s.name]
    df_muni = ( df
                [ df["muni code"] == muni ]
                [["year","item categ", s.pesos_col]] )
    df_pivot = (
      df_muni .
      pivot( index = "item categ",
             columns = "year",
             values = s.pesos_col ) .
      fillna( 0 ) )
    df_pivot = df_pivot.astype(int) # TODO : this should happen upstream
    dest = 'output/reports/' + str(muni)
    if not os.path.exists( dest ):
      os.makedirs( dest )
    with PdfPages( dest + "/" + s.name + ".pdf" ) as pdf:
      lib.drawPage( df_pivot, ["Title?"], ["Text?"] )
      pdf.savefig( facecolor=lib.background_color )
      plt.close()

with open( "output/reports/done.txt", "w" ) as f:
  f.write( "done" )
