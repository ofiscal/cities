# import matplotlib as plt
import numpy as np
import pandas as pd


df = pd.read_csv( "data.csv", index_col=0 )
nCols = len( df.columns )
nRows = len( df.index )
xvals = np.arange( len( df.columns ) )

plots = {}
for rn in range(nRows):
  if rn < 1: bottom = None
  else: bottom =  df.iloc[rn-1,:]
  plots[rn] = plt.bar(
      xvals
    , df.iloc[rn,:]
    , width = [0.5 for i in range( nCols )]
    , bottom=bottom )

plt.title('Cool Stuff')
plt.ylabel('How Much')
plt.xticks(xvals, df.columns )
frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
plt.legend( plots.values(), df.index )

plt.show()
