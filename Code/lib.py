import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd


def drawPage( folder ):
  df = pd.read_csv( folder + "/data.csv", index_col=0 )
  with open( folder + "/text.txt", "r") as myfile:
      lines = myfile.readlines()
  plt.subplots(2, 1)
  (    plt.subplot(2, 1, 1))
  drawText( lines )
  ax = plt.subplot(2, 1, 2)
  drawStacks( ax, df )

def drawText( lines ):
  plt.text( 0, 0.5
          , "".join( lines )
          , fontproperties =
            fm.FontProperties(fname=font_light)
          , verticalalignment="center" )

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
               , horizontalalignment='center' )

    plt.legend( plots.values(), df.index )
    del(bottom, plots)

  if True: # add labels
    # Vertical axis needs a label, but no ticks, and no tick labels. Based on
    # https://stackoverflow.com/questions/29988241/python-hide-ticks-but-show-tick-labels
    ax.set( title='Cool Stuff'
          , xlabel="Year"
          , ylabel='Real spending (2019 pesos)' )
    plt.xticks( xvals, df.columns )
    plt.setp( ax.get_yticklabels()
            , visible=False )
    ax.tick_params( axis='y', which='both', length=0 )

font_black = "fonts/Montserrat_Black.ttf"
font_light = "fonts/Montserrat_Light.ttf"
