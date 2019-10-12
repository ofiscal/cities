if True:
  import matplotlib.pyplot as plt
  import numpy as np
  import pandas as pd

def brief( # a utility to display numbmers briefly,
           # to (roughly) 3 significant digits
    f : float ) -> str:
  if abs(f) < 0.001: return "0"
  else: return ( "{0:.3g}" . format( f ) )

# the dimensions and contents of the data
df = pd.DataFrame( [ [3,1,2],
                     [1,2,3],
                     [2,3,1] ] )
nCols : int = len( df.columns )
nRows : int = len( df.index )

# Make space to draw
plt.subplots( 1, 1 )
ax = plt.subplot( 1, 1, 1 )

for rn in range( nRows ):
  # Plot one row after the other.
  # The bars in each row are the same color.
  if True: # These series describe the vertical
           # dimensions of row `rn` of bars
    if rn < 1: bottom = df.iloc[0,   :]*0 # a row of zeros
    else:      bottom = df.iloc[0:rn,:].sum()
    height = df.iloc[  rn,:]
  ax.bar( # draw the bars
    np.arange( nCols ),
    height,
    width = [ 0.8 for i in range( nCols ) ],
    bottom = bottom )

for rn in range( nRows ):
  # Plot one row after the other.
  # The bars in each row are the same color.
  if True: # These series describe the vertical
           # dimensions of row `rn` of bars
    if rn < 1: bottom = df.iloc[0,   :]*0 # a row of zeros
    else:      bottom = df.iloc[0:rn,:].sum()
    height = df.iloc[  rn,:]
    top = bottom + height
    middle = (bottom + top) / 2 # halfway from the bottom to the top
  for cn in range( nCols ): # write text on each bar
    if True: # for for a single bar, translate its bottom,
      # height and top into the axes coordinate system.
      # First transform from data to display coordinates,
      # then from display to axes coordinates.
      bottom_in_axes = ( ax.transAxes.inverted().transform(
                           ax.transData.transform(( 0, bottom[cn] )) )
                         [1] )
      height_in_axes = ( ax.transAxes.inverted().transform(
                           ax.transData.transform(( 0, height[cn] )) )
                           [1] )
      top_in_axes    = ( ax.transAxes.inverted().transform(
                           ax.transData.transform(( 0, top[cn] )) )
                         [1] )
    ax.text( # write text on each bar
      float( cn ), 
      middle.iloc[cn],
      ( "Bottom, height, top:\n" +
        "Data: " +
        str( bottom[cn] ) + ", " +
        str( height[cn] ) + ", " +
        str( top[cn] ) + "\n" +
        "Axes: " +
        brief( bottom_in_axes ) + ", " +
        brief( height_in_axes ) + ", " +
        brief( top_in_axes ) ),
      verticalalignment = 'center',
      horizontalalignment = 'center',
      fontsize = 7 )

plt.savefig( "bars.png", format = "png" )
