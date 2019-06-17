import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd


def drawPage( folder ):
  df = pd.read_csv( folder + "/data.csv", index_col=0 )
  with open( folder + "/text.txt", "r") as myfile:
      lines = myfile.readlines()
  plt.subplots(2, 1)
  ax = plt.subplot(2, 1, 1)
  drawText( ax, lines )
  ax = plt.subplot(2, 1, 2)
  drawStacks( ax, df )

def drawText( ax, lines ):
  plt.text( 0, 0.5
          , "".join( lines )
          , fontproperties = font_light
          , verticalalignment="center" )
  ax.axis('off')

def drawStacks( ax, df ):
  nCols = len( df.columns )
  nRows = len( df.index )
  xvals = np.arange( nCols )

  if True: # draw stuff
    plots = {}
    for rn in range(nRows):
      if rn < 1: bottom = [0. for i in range(nCols)]
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
               , fontsize=10
               , verticalalignment='center'
               , horizontalalignment='center'
               , fontproperties = font_light )

    plt.legend( plots.values()
              , df.index
              , prop = font_light )
    del(bottom, plots)

  if True: # add labels
    # Vertical axis needs a label, but no ticks, and no tick labels. Based on
    # https://stackoverflow.com/questions/29988241/python-hide-ticks-but-show-tick-labels
    ax.set_title( "Cool stufff"
                , fontproperties = font_light )
    ax.set_xlabel( "Year"
                 , fontproperties = font_light )
    ax.set_ylabel( 'Real spending (2019 pesos)'
                 , fontproperties = font_light )

    plt.xticks( xvals, df.columns )
    plt.setp( ax.get_xticklabels(), visible=False )
    plt.setp( ax.get_yticklabels(), visible=False )
    ax.tick_params( axis='x', which='both', length=0 )
    ax.tick_params( axis='y', which='both', length=0 )
    ax.set_frame_on(False)

font_black = fm.FontProperties( fname = "fonts/Montserrat_Black.ttf" )
font_light = fm.FontProperties( fname = "fonts/Montserrat_Light.ttf" )
