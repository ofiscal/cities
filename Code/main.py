import os
import pandas as pd
import matplotlib.pyplot as plt
from   matplotlib.backends.backend_pdf import PdfPages

import Code.common as c
import Code.build.sisfut_metadata as sm
import Code.draw.lib as lib


source = "output/conceptos_4_top_categs_only_and_scaled/recip-" + str(c.subsample)

dfs = {}
for s in sm.series:
  df = pd.read_csv( source + "/" + s + ".csv" )
  dfs[s] = df

for s in ["ingresos"]:
  for muni in [15764]:
    df = dfs[s]
    df_muni = ( df
                [ df["muni code"] == muni ]
                [["year","item", "item recaudo"]] )
    df_pivot = (
      df_muni .
      pivot( index = "item",
             columns = "year",
             values = "item recaudo" ) .
      astype(int) ) # TODO : this should happen upstream
    if True: # This is to make df_pivot resemble the example.
      # It doesn't seem to help.
      df_pivot.index.name = None
      df_pivot.columns.name = None
    dest = 'output/reports/' + str(muni)
    if not os.path.exists( dest ):
      os.makedirs( dest )
    with PdfPages( dest + "/" + s + ".pdf" ) as pdf:
      lib.drawPage( df_pivot, ["Title?"], ["Text?"] )
      pdf.savefig( facecolor=lib.background_color )
      plt.close()

