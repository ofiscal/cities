if True:
  import os
  from   pathlib import Path
  import pandas as pd
  import matplotlib.pyplot as plt
  from   matplotlib.backends.backend_pdf import PdfPages
  #
  import Code.common as c
  import Code.metadata.four_series as s4
  import Code.build.use_keys as uk
  import Code.draw.lib as lib

root = "output/pivots/recip-" + str(c.subsample)

if True: # create geo indices to loop over
  geo = uk.merge_geo( # Using stage 6p7 rather than 7 because
    pd.read_csv(      # they are equivalent and it's smaller
      ( "output/budget_6p7_avg_muni/recip-" + str(c.subsample) +
        "/" + "gastos-pct.csv" ),
      usecols = ['dept code', 'muni code'] ) .
    drop_duplicates() .
    reset_index( drop=True ) .
    sort_values( ["dept code","muni code"] ) )
  geo.loc[ geo["muni code"]==0,
           "muni" ] = "dept"
  geo.loc[ geo["muni code"]==-2,
           "muni" ] = "promedio"

def create_pdfs( dept : str,
                 muni : str ):
 folder = ( root + "/" + dept + "/" + muni )
 print("folder: ", folder)
 for file in ( s4.series_pct
               if muni == "promedio"
               else s4.series ):
   pivot = (
     pd.read_csv(
       folder + "/" + file.name + ".csv",
       index_col="item categ" ) )
   with PdfPages( folder + "/" + file.name + ".pdf" ) as pdf:
     lib.drawPage( pivot, ["Title?"], ["Text?"] )
     pdf.savefig( facecolor=lib.background_color )
     plt.close()

geo.apply(
  ( lambda row:
    create_pdfs( dept = row["dept"],
                 muni = row["muni"] ) ),
  axis = "columns" )

( Path( root + "/" + "timestamp-for-pdfs" ) .
  touch() )

