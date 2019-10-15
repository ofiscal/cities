if True:
  from typing import List, Set, Dict
  import pandas as pd
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  import matplotlib.image as mpimg
  #
  import Code.common as c
  import Code.draw.chart.time_series as ts
  import Code.draw.chart.pairs as pairs
  import Code.draw.design as design


def drawTitlePage( muni : str,
                   pdf ):
  # The default figure size has to be increased in order for .png import
  # not to be horribly grainy.
  plt.rcParams.update({'figure.figsize': (38,24)})

  # The figure is divided into 4 rows (and 1 column).
  # The first row goes to the image;
  # the rest, to the text.
  fig = plt.figure(
    constrained_layout=False,
    facecolor = design.background_color)
  grid = fig.add_gridspec(nrows=4, ncols=1)

  ax1 = fig.add_subplot(grid[0, :])
  ax1.axis( 'off' )
  img = mpimg.imread('design/Logo_Ofiscal_blanco_horiz.png')
  imgplot = ax1.imshow( img )
  plt.imshow(img)

  ax2 = fig.add_subplot(grid[1:, :])
  ax2.axis( 'off' )
  plt.text(
    0.5, 0.5,
    "\n".join(
      [ "¿En qué se gasta", "la plata",
        muni + "?" ]),
    transform = ax2.transAxes,
    color = design.orange,
    fontproperties = design.font_thick,
    fontsize = design.sizeText_title,
    verticalalignment="center",
    horizontalalignment="center")
  pdf.savefig( facecolor = design.dark_blue )
  plt.close()

def drawTextAboveChart( ax : mplot.axes.SubplotBase,
                        title : List[str],
                        text : List[str] ):
  plt.text( 0.5, 0.9,
            "\n".join( title ),
            color = 'k',
            fontproperties = design.font_thick,
            fontsize = design.sizeText_chartPage,
            horizontalalignment="center" )
  plt.text( 0, 0.5,
            "\n".join( text ),
            color = 'k',
            fontproperties = design.font_thin,
            fontsize = design.sizeText_chartBody,
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
    fontsize = design.sizeText_zenPageTitle,
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
    fontsize = design.sizeText_zenPageBody,
    verticalalignment="center" )

  plt.text(
    0, 0.1,
    "Su voto determina quien va a manejar los recursos del municipio. ¡Vote!",
    color = 'k',
    fontproperties = design.font_thin,
    fontsize = design.sizeText_zenPageBody,
    verticalalignment="center" )

  ax.axis( 'off' )
  pdf.savefig( facecolor=design.background_color )
  plt.close()

