# PITFALL: Matplotlib is very imperative,
# so the order of function calls matters greatly.

if True:
  from typing import List, Set, Dict
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  import matplotlib.font_manager as fm
  import numpy as np
  import pandas as pd
  #
  import Code.draw.design as design
  import Code.draw.text.shorten_numbers as abbrev

def drawStacks( ax : mplot.axes.SubplotBase,
                df : pd.DataFrame ):
  df = df . iloc[::-1] # Revserse column order.
    # In the bar chart, each row is drawn on top of the previous one.
    # This reversal causes earlier ("higher")
    # rows to be drawn above later ones,
    # which means vertical order of items in the chart corresponds to
    # the vertical order of items in the data file.
    # It's a nuance the chart would still make sense without.
  if True: # the dimensions and contents of the data
    nCols : int = len( df.columns )
    nRows : int = len( df.index )
    xvals : np.ndarray = np.arange( nCols )
  if True: # how to show numbers
    commas = abbrev.commas( df.max().max() )
    units = abbrev.units( commas )
  if True: # procedures
    plots = add_plots( # PITFALL: side effects *and* a return value
      nCols, nRows, xvals, commas, ax, df )
    add_legend      (ax, plots, df)
    add_outer_labels(ax, xvals, units, df)

def add_plots( nCols : int,
               nRows : int,
               xvals : np.ndarray,
               commas : int,
               ax : mplot.axes.SubplotBase,
               df : pd.DataFrame
             ) -> List[mplot.container.Container]:
  plots = [] # This is what gets returned.
  for rn in range( nRows ):
    if True: # PITFALL: while "bottom" is absolute,
             # "height" is relative to "bottom".
      if rn < 1: bottom = df.iloc[0,   :]*0 # just a row of zeros
      else:      bottom = df.iloc[0:rn,:].sum()
      height = df.iloc[  rn,:]
    plots.insert( 0, # prepend => legend items in the right order
                  ax.bar( xvals, # plot stack of bar charts
                          height,
                          width = [ 0.3 for i in range( nCols ) ],
                          bottom = bottom ) )
  for rn in range( nRows ):
    # The computation of bottom and height is equal to
    # that iin the previous loop. They cannot be joined, though,
    # because it would ruin the `*_in_axes` variables below,
    # because each time the first loop calls ax.bar(),
    # the vertical range of the image changes;
    if True:
      if rn < 1: bottom = df.iloc[0,   :]*0 # just a row of zeros
      else:      bottom = df.iloc[0:rn,:].sum()
      height = df.iloc[  rn,:]
      top = bottom + height
    middle = (bottom + top) / 2
    enough_to_print = float( ax.transData.inverted().transform(
                               ax.transAxes.transform(( 0,0.2 )) )
                             [1] )
    for cn in range( nCols ): # plot amounts in each box
      height_in_axes = ( ax.transAxes.inverted().transform(
                           ax.transData.transform(( 0, height[cn] )) )
                         [1] )
      if height_in_axes > 0.05:
        ax.text( float( cn ),
                 middle.iloc[cn],
                 abbrev.show_brief( # what we're printing
                   df.iloc[ rn, cn ],
                   commas ),
                 verticalalignment = 'center',
                 horizontalalignment = 'center',
                 color = 'w',
                 fontproperties = design.font_thin,
                 fontsize = 6 )
  for cn in range( nCols ): # plot totals above each column
    total = df.iloc[:,cn].sum()
    buffer = ( # Convert 0.04 from axes coords to screen coords,
               # and then from screen coords to data coords.
      ax.transData.inverted().transform(
        ax.transAxes.transform( (0,0.04) ) )
      [1] )
    ax.text( float( cn ),
             total + buffer,
             abbrev.show_brief( # what we're printing
               total, commas ),
             verticalalignment = 'center',
             horizontalalignment = 'center',
             color = 'w',
             fontproperties = design.font_thin,
             fontsize = 8 )
  return plots

def add_legend(
    ax : mplot.axes.SubplotBase,
    plots : List[mplot.container.Container], # list of bar charts
    df : pd.DataFrame ):
  plt.rcParams['axes.titlepad'] = 10
  chartBox = ax.get_position()
  ax.set_position([ chartBox.x0,
                    chartBox.y0,
                    chartBox.width*0.6,
                    chartBox.height ])
  leg = ax.legend(
    plots,
    reversed( df.index ), # to match the order of `plots`
    prop = fm.FontProperties( # PITFALL: This cannot be simplified.
        # Incredibly, if we first define
        #     def font_light_func( size : int ):
        #       fm.FontProperties( fname = "fonts/Montserrat_Light.ttf",
        #                          size = size )
        # and then replace the above `prop = fm.FontProperties(...)` call
        # with `prop = font_light_func(6)`, it behaves differently,
        # in particular using a huge font size.
      fname = "design/Montserrat_Light.ttf",
      size = 7),
    facecolor = design.background_color,
    shadow=True,

    # The next arguments:
    # draw the legend to the right of the plot, ala
    # https://pythonspot.com/matplotlib-legend/
    loc = 'upper center',
    bbox_to_anchor = ( 1.45, 0.8 ),
    ncol = 1 )
  plt.setp( leg.get_texts(),
            color = 'k' )

def add_outer_labels( ax : mplot.axes.SubplotBase,
                      xvals : np.ndarray,
                      units : str,
                      df : pd.DataFrame ):
  """Give vertical axis a label, no ticks, no tick labels. Based on
stackoverflow.com/questions/29988241/python-hide-ticks-but-show-tick-labels
"""
  ax.set_xlabel( "Year",
                 color = 'k',
                 fontproperties = design.font_thin )
  ax.set_ylabel( units,
                 color = 'k',
                 fontproperties = design.font_thin )

  plt.xticks( xvals, df.columns )
  plt.setp( ax.get_xticklabels(),
            visible = True,
            color = 'k',
            fontproperties = design.font_thin )
  plt.setp( ax.get_yticklabels(), visible = False )
  ax.tick_params( axis='x', which='both', length=0 )
  ax.tick_params( axis='y', which='both', length=0 )
  ax.set_frame_on(False)

