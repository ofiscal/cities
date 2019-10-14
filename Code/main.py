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
  import Code.draw.pairs as pairs
  import Code.draw.style as style
  import Code.draw.newlines as newlines

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

def drawTitlePage( muni : str,
                   pdf ):
  plt.subplots( 2, 1, facecolor = style.background_color )
  ax = plt.subplot( 1, 1, 1 )
  text = [ "¿En qué se gasta",
           "la plata",
           muni + "?" ]
  plt.text( 0.5, 0.5,
            "\n".join( text ),
            transform = ax.transAxes,
            color = 'k',
            fontproperties = style.font_thick,
            fontsize = 30,
            verticalalignment="center",
            horizontalalignment="center")
  ax.axis( 'off' )
  pdf.savefig( facecolor=style.background_color )
  plt.close()

def drawPageWithChart( df : pd.DataFrame,
                       title : List[str],
                       text : List[str],
                       pdf,
                       drawChart ): # a callback
  plt.subplots( 2, 1, facecolor = style.background_color )
  ax = plt.subplot( 2, 1, 1 )
  drawText( ax, title, text )
  ax = plt.subplot( 2, 1, 2 )
  drawChart( ax, df )
  pdf.savefig( facecolor=style.background_color )
  plt.close()

def create_pdf( dept : str,
                muni : str ):
  folder = ( root + "/" + dept + "/" + muni )
  print("folder: ", folder)
  with PdfPages( folder + "/report.pdf" ) as pdf:
    drawTitlePage( muni, pdf )
    for  (file,                insertNewlines, index_col,    drawChart) in [
         ("ingresos-pct-compare", True,        0,            pairs.drawPairs),
         ("gastos-pct-compare",   True,        0,            pairs.drawPairs),
         ("ingresos",             False,       "item categ", ts.drawStacks),
         ("gastos",               False,       "item categ", ts.drawStacks) ]:
      df = pd.read_csv(
        folder + "/" + file + ".csv",
        index_col = index_col )
      if insertNewlines:
        df.index = list( map( lambda s: newlines.remap[s],
                              df.index ) )
      drawPageWithChart( df,
                         ["Title?"],
                         ["Text?"],
                         pdf,
                         drawChart )

geo.apply(
  ( lambda row:
    create_pdf( dept = row["dept"],
                muni = row["muni"] ) ),
  axis = "columns" )

( Path( root + "/" + "timestamp-for-pdfs" ) .
  touch() )

