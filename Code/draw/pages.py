if True:
  from typing import List, Set, Dict
  import pandas as pd
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  #
  import Code.common as c
  import Code.draw.chart.time_series as ts
  import Code.draw.chart.pairs as pairs
  import Code.draw.design as design


def drawTitlePage( muni : str,
                   pdf ):
  plt.subplots( 2, 1, facecolor = design.background_color )
  ax = plt.subplot( 1, 1, 1 )
  plt.text(
    0.5, 0.5,
    "\n".join(
      [ "¿En qué se gasta", "la plata",
        muni + "?" ]),
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
            fontsize=14,
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

  # Create a 4-row, 1-column grid over the figure.
  # The bottom three rows will go to the chart,
  # and the top one to the text. See
  # https://matplotlib.org/tutorials/intermediate/gridspec.html
  fig = plt.figure(
    constrained_layout=False,
    facecolor = design.background_color)
  grid = fig.add_gridspec(nrows=4, ncols=1)

  ax1 = fig.add_subplot(grid[0, :])
  drawTextAboveChart( ax1, title, text )
  ax2 = fig.add_subplot(grid[1:, :])
  drawChart( ax2, df )

  pdf.savefig( facecolor=design.background_color )
  plt.close()

def drawZenQuestions( muni : str,
                      pdf ):
  plt.subplots( 2, 1, facecolor = design.background_color )
  ax = plt.subplot( 1, 1, 1 )

  plt.text(
    0.5, 0.9,
    "\n".join(
      [ "Como ciudadano de " + muni + ", usted puede observar",
        "el desempeño del gobierno municipal mejor que nadie." ] ),
    color = 'k',
    fontproperties = design.font_thick,
    fontsize = 14,
    horizontalalignment="center" )

  plt.text(
    0, 0.5,
    "\n".join(
      [ "¿Se están gastando adecuadamente los recursos del municipio?",
        "",
        "¿Qué promesas están haciendo los candidatos?",
        "",
        "¿Sí alcanza la plata para lo que están prometiendo?",
        "",
        "¿Qué gastos habría que recortar?",
        "",
        "¿Qué ingresos tendrían que subir?" ] ),
    color = 'k',
    fontproperties = design.font_thin,
    verticalalignment="center" )

  plt.text(
    0, 0.1,
    "Su voto determina quien va a manejar los recursos del municipio. ¡Vote!",
    color = 'k',
    fontproperties = design.font_thin,
    verticalalignment="center" )

  ax.axis( 'off' )
  pdf.savefig( facecolor=design.background_color )
  plt.close()

