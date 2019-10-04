import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd


font_black = "fonts/Montserrat_Black.ttf"
font_light = "fonts/Montserrat_Light.ttf"

def drawText( text ):
  plt.text( 0.5, 0.5, text
          , fontproperties =
            fm.FontProperties(fname=font_black) )
drawText( "Wuz hatnen?" )
plt.show()


df = pd.DataFrame( { "2014": [1,2,3,4]
                   , "2015": [3,4,5,1] }
                 , index=["Saturn","hedgehog","abstract","crunk"] )

def drawStacks( df ):
  _,ax = plt.subplots()
  nCols = len( df.columns )
  nRows = len( df.index )
  xvals = np.arange( nCols )

  if True: # Draw stuff.
    plots = {}
    for rn in range(nRows):
      if True: # These details are not important to my question.
        if rn < 1: bottom = [0. for i in range(nCols)]
        else:      bottom = df.iloc[0:rn,:].sum()
        top =      bottom + df.iloc[  rn,:]
        plots[rn] = ax.bar(
            xvals
          , df.iloc[rn,:]
          , width = [ 0.8 for i in range( nCols ) ]
          , bottom = bottom )
      for cn in range( nCols ): # One kind of text
        ax.text( float( cn )
               , ((bottom + top) / 2)[cn]
               , df.iloc[ rn, cn ]
               , fontsize=10
               , verticalalignment='center'
               , horizontalalignment='center' )

  plt.legend( plots.values(), df.index )        # Another kind of text
  ax.set( title="What it is"                    # Another kind of text
        , xlabel="Year"                         # Another kind of text
        , ylabel='Real spending (2019 pesos)' ) # Another kind of text

drawStacks( df )
plt.show()
