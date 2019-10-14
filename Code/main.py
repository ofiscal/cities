if True:
  import os
  from typing import List, Set, Dict
  from   pathlib import Path
  import pandas as pd
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  from   matplotlib.backends.backend_pdf import PdfPages
  #
  import Code.common as c
  import Code.metadata.four_series as s4
  import Code.build.use_keys as uk
  import Code.draw.time_series as ts
  import Code.draw.style as style

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
  geo = geo[ geo["muni code"] > 0 ]
  # geo.loc[ geo["muni code"]==0,
  #          "muni" ] = "dept"
  # geo.loc[ geo["muni code"]==-2,
  #          "muni" ] = "promedio"

def drawText( ax : mplot.axes.SubplotBase,
              title : List[str],
              text : List[str] ):
  plt.text( 0.5, 0.9,
            "".join( title ),
            color = 'k',
            fontproperties = style.font_thick,
            horizontalalignment="center" )
  plt.text( 0, 0.5,
            "".join( text ),
            color = 'k',
            fontproperties = style.font_thin,
            verticalalignment="center" )
  ax.axis( 'off' )

def drawPage( df : pd.DataFrame,
              title : List[str],
              text : List[str],
              drawChart ): # a callback
  plt.subplots( 2, 1, facecolor = style.background_color )
  ax = plt.subplot( 2, 1, 1 )
  drawText( ax, title, text )
  ax = plt.subplot( 2, 1, 2 )
  drawChart( ax, df )

def create_pdf( dept : str,
                muni : str ):
  folder = ( root + "/" + dept + "/" + muni )
  print("folder: ", folder)
  for file in s4.series:
    pivot = (
      pd.read_csv(
        folder + "/" + file.name + ".csv",
        index_col="item categ" ) )
    with PdfPages( folder + "/" + file.name + ".pdf" ) as pdf:
      drawPage( pivot,
                ["Title?"],
                ["Text?"],
                ts.drawStacks )
      pdf.savefig( facecolor=style.background_color )
      plt.close()

geo.apply(
  ( lambda row:
    create_pdf( dept = row["dept"],
                muni = row["muni"] ) ),
  axis = "columns" )

( Path( root + "/" + "timestamp-for-pdfs" ) .
  touch() )

