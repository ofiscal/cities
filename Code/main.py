if True:
  import os
  import pandas as pd
  import matplotlib.pyplot as plt
  from   matplotlib.backends.backend_pdf import PdfPages
  #
  import Code.common as c
  import Code.metadata.two_series as ser
  import Code.build.use_keys as uk
  import Code.draw.lib as lib

def create_pdfs( dept : str,
                 muni : str ):
 folder = ( "output/pivots/recip-" + str(c.subsample) +
            "/" + dept + "/" + muni )
 print("folder: ", folder)
 for file in ser.series:
   pivot = (
     pd.read_csv(
       folder + "/" + file.name + ".csv",
       index_col="item categ" ) .
     fillna( 0 ) ) # TODO : should not be necessary.
                   # Fix upstream, in budget_8.
   with PdfPages( folder + "/" + file.name + ".pdf" ) as pdf:
     lib.drawPage( pivot, ["Title?"], ["Text?"] )
     pdf.savefig( facecolor=lib.background_color )
     plt.close()

uk.depts_and_munis.apply(
  ( lambda row:
    create_pdfs( row["dept"],
                 row["muni"] ) ),
  axis = "columns" )

with open( "output/reports/done.txt", "w" ) as f:
  f.write( "done" )

