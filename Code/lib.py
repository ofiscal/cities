import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd


def drawPage( folder ):
  df = pd.read_csv( folder + "/data.csv", index_col=0 )
  with open( folder + "/text.txt", "r") as myfile:
      lines = myfile.readlines()
  plt.subplots( 2, 1, facecolor=background_color )
  ax = plt.subplot( 2, 1, 1 )
  drawText( ax, lines )
  ax = plt.subplot( 2, 1, 2 )
  drawStacks( ax, df )

def drawText( ax, lines ):
  plt.text( 0, 0.5
          , "".join( lines )
          , color = 'k'
          , fontproperties = font_light
          , verticalalignment="center" )
  ax.axis( 'off' )

def drawStacks( ax, df ):
  nCols = len( df.columns )
  nRows = len( df.index )
  xvals = np.arange( nCols )

  if True: # draw stuff
    plots = {}
    for rn in range( nRows ):
      if rn < 1: bottom = [0. for i in range( nCols )]
      else:      bottom = df.iloc[0:rn,:].sum()
      top =      bottom + df.iloc[  rn,:]
      plots[rn] = ax.bar(
          xvals
        , df.iloc[rn,:]
        , width = [ 0.8 for i in range( nCols ) ]
        , bottom = bottom )
      for cn in range( nCols ): # TODO ? speed: use pd.Seeries.iteritems().
        ax.text( float( cn )
               , ((bottom + top) / 2)[cn]
               , df.iloc[ rn, cn ]
               , fontsize = 10
               , verticalalignment = 'center'
               , horizontalalignment = 'center'
               , color = 'w'
               , fontproperties = font_light )

    chartBox = ax.get_position()
    ax.set_position([ chartBox.x0
                    , chartBox.y0
                    , chartBox.width*0.6
                    , chartBox.height ])

    leg = plt.legend( plots.values()
                    , df.index
                    , prop = font_light
                    , facecolor = background_color
                    , shadow=True
            # Next arguments: draw the legend to the right of the plot, ala
            # https://pythonspot.com/matplotlib-legend/
                    , loc = 'upper center'
                    , bbox_to_anchor = ( 1.45, 0.8 )
                    , ncol = 1 )
    plt.setp( leg.get_texts()
            , color = 'k' )

    del( bottom, chartBox, leg, plots )

  if True: # add labels
    # Vertical axis needs a label, but no ticks, and no tick labels. Based on
    # https://stackoverflow.com/questions/29988241/python-hide-ticks-but-show-tick-labels
    ax.set_title( "Cool stuff"
                , color = 'k'
                , fontproperties = font_light )
    ax.set_xlabel( "Year"
                 , color = 'k'
                 , fontproperties = font_light )
    ax.set_ylabel( 'Real spending (2019 pesos)'
                 , color = 'k'
                 , fontproperties = font_light )

    plt.xticks( xvals, df.columns )
    plt.setp( ax.get_xticklabels()
            , visible = True
            , color = 'k'
            , fontproperties = font_light )
    plt.setp( ax.get_yticklabels(), visible = False )
    ax.tick_params( axis='x', which='both', length=0 )
    ax.tick_params( axis='y', which='both', length=0 )
    ax.set_frame_on(False)

background_color = "xkcd:salmon"
font_black = fm.FontProperties( fname = "fonts/Montserrat_Black.ttf" )
font_light = fm.FontProperties( fname = "fonts/Montserrat_Light.ttf" )
