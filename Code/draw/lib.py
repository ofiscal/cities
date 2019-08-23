from typing import List
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import numpy as np
import pandas as pd


def drawPage( df : pd.DataFrame,
              title : List[str],
              text : List[str] ):
  df = df . iloc[::-1] # Revserse column order.
    # In the bar chart, each row is drawn on top of the previous one.
    # This reversal causes earlier ("higher") rows to be drawn above later ones,
    # which means vertical order of items in the chart corresponds to
    # the vertical order of items in the data file.
    # It's a nuance the chart would still make sense without.
  plt.subplots( 2, 1, facecolor = background_color )
  ax = plt.subplot( 2, 1, 1 )
  drawText( ax, title, text )
  ax = plt.subplot( 2, 1, 2 )
  drawStacks( ax, df )

def drawText( ax, # : matplotlib.axes.SubplotBase
              title : List[str],
              text : List[str] ):
  plt.text( 0.5, 0.9
          , "".join( title )
          , color = 'k'
          , fontproperties = font_black
          , horizontalalignment="center" )
  plt.text( 0, 0.5
          , "".join( text )
          , color = 'k'
          , fontproperties = font_light
          , verticalalignment="center" )
  ax.axis( 'off' )

def drawStacks( ax, # : matplotlib.axes.SubplotBase
                df : pd.DataFrame ):
  nCols = len( df.columns )
  nRows = len( df.index )
  xvals = np.arange( nCols )

  if True: # draw stuff
    plots = []
    for rn in range( nRows ):
      # bottom, top are both series describing that row's bars
      if rn < 1: bottom = [0. for i in range( nCols )]
      else:      bottom = df.iloc[0:rn,:].sum()
      top =      bottom + df.iloc[  rn,:]
      plots.insert( 0 # prepend => legend items in the right order
                  , ax.bar( xvals # plot stack of bar charts
                          , df.iloc[rn,:]
                          , width = [ 0.8 for i in range( nCols ) ]
                          , bottom = bottom ) )
      print( "\nrow",rn,"bottom:\n",bottom,"top:\n",top )
      for cn in range( nCols ): # plot amounts over each box
        # todo ? speed: use pd.Seeries.iteritems()
        ax.text( float( cn )
               , ((bottom + top) / 2)[cn]
               , df.iloc[ rn, cn ]   # what we're printing
               , fontsize = 10
               , verticalalignment = 'center'
               , horizontalalignment = 'center'
               , color = 'w'
               , fontproperties = font_light )
    for cn in range( nCols ): # plot totals above each column
        total = df.iloc[:,cn].sum()
        ax.text( float( cn )
               , total + 1
               , total
               , fontsize = 10
               , verticalalignment = 'center'
               , horizontalalignment = 'center'
               , color = 'w'
               , fontproperties = font_light )

    plt.rcParams['axes.titlepad'] = 10
    chartBox = ax.get_position()
    ax.set_position([ chartBox.x0
                    , chartBox.y0
                    , chartBox.width*0.6
                    , chartBox.height ])

    leg = ax.legend( plots
                   , reversed( df.index ) # to match the order of `plots`
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

  if True: # add (outer) labels
    # Vertical axis needs a label, but no ticks, and no tick labels. Based on
    # https://stackoverflow.com/questions/29988241/python-hide-ticks-but-show-tick-labels
    ax.set_title( "Cool stuff"
                , color = 'k'
                , fontproperties = font_black )
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

background_color = "mediumaquamarine"
font_black = fm.FontProperties( fname = "fonts/Montserrat_Black.ttf" )
font_light = fm.FontProperties( fname = "fonts/Montserrat_Light.ttf" )
