if True:
  from typing import List, Set, Dict
  import pandas as pd
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  #
  import Code.common as c
  import Code.draw.time_series as ts
  import Code.draw.pairs as pairs
  import Code.draw.design as design


def drawTitlePage( muni : str,
                   pdf ):
  plt.subplots( 2, 1, facecolor = design.background_color )
  ax = plt.subplot( 1, 1, 1 )
  text = [ "¿En qué se gasta",
           "la plata",
           muni + "?" ]
  plt.text( 0.5, 0.5,
            "\n".join( text ),
            transform = ax.transAxes,
            color = 'k',
            fontproperties = design.font_thick,
            fontsize = 30,
            verticalalignment="center",
            horizontalalignment="center")
  ax.axis( 'off' )
  pdf.savefig( facecolor=design.background_color )
  plt.close()

def drawTextAboveChart( ax : mplot.axes.SubplotBase,
                        title : List[str],
                        text : List[str] ):
  plt.text( 0.5, 0.9,
            "\n".join( title ),
            color = 'k',
            fontproperties = design.font_thick,
            horizontalalignment="center" )
  plt.text( 0, 0.5,
            "\n".join( text ),
            color = 'k',
            fontproperties = design.font_thin,
            verticalalignment="center" )
  ax.axis( 'off' )

def drawPageWithChart( df : pd.DataFrame,
                       title : List[str],
                       text : List[str],
                       pdf,
                       drawChart ): # a callback
  plt.subplots( 2, 1, facecolor = design.background_color )
  ax = plt.subplot( 2, 1, 1 )
  drawTextAboveChart( ax, title, text )
  ax = plt.subplot( 2, 1, 2 )
  drawChart( ax, df )
  pdf.savefig( facecolor=design.background_color )
  plt.close()
