import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def drawStacks( df ):
  nCols = len( df.columns )
  nRows = len( df.index )
  xvals = np.arange( nCols )
  
  if True: # draw stuff
    fig, (ax) = plt.subplots() # or subplots(1,1)
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
