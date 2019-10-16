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
                background_color : str,
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
      background_color,
      nCols, nRows, xvals, commas, ax, df )
    add_legend      (ax, background_color, plots, df)
    add_outer_labels(ax, xvals, units, df)

def add_plots(
    background_color : str,
    nCols : int,
    nRows : int,
    xvals : np.ndarray,
    commas : int,
    ax : mplot.axes.SubplotBase,
    df : pd.DataFrame
    ) -> List[mplot.container.Container]:
  plots = [] # This is what gets returned.
  totals = df.sum()

  for rn in range( nRows ): # draw bars
    if True: # PITFALL: while "bottom" is absolute,
             # "height" is relative to "bottom".
      if rn < 1: bottom = df.iloc[0,   :]*0 # just a row of zeros
      else:      bottom = df.iloc[0:rn,:].sum()
      height = df.iloc[  rn,:]
    plots.insert(
      0, # prepend => legend items in the right order
      ax.bar( xvals, # plot stack of bar charts
              height,
              width = [ design.sizeBarWidth for i in range( nCols ) ],
              bottom = bottom ) )

  for rn in range( nRows ): # plot percentages next to each bar
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
    for cn in range( nCols ):
      height_in_axes = ( ax.transAxes.inverted().transform(
                           ax.transData.transform(( 0, height[cn] )) )
                         [1] )
      if height_in_axes > 0.025:
        ax.text( float( cn ) + 1.2 * design.sizeBarWidth,
                 middle.iloc[cn],
                 ( abbrev.show_brief( # what we're printing
                     100 * df.iloc[ rn, cn ] / totals[cn],
                     0 )
                   + "%"),
                 verticalalignment = 'center',
                 horizontalalignment = 'center',
                 color = design.against( background_color ),
                 fontproperties = design.font_thin,
                 fontsize = design.sizeText_inBars )

  for cn in range( nCols ): # plot totals above each column
    buffer = ( # Convert 0.04 from axes coords to screen coords,
               # and then from screen coords to data coords.
      ax.transData.inverted().transform(
        ax.transAxes.transform( (0,0.04) ) )
      [1] )
    ax.text( float( cn ),
             totals[cn] + buffer,
             "$" + abbrev.show_brief( # what we're printing
               totals[cn], commas ),
             verticalalignment = 'center',
             horizontalalignment = 'center',
             color = design.orange,
             fontproperties = design.font_thin,
             fontsize = design.sizeText_aboveBars )
  return plots

def add_legend(
    ax : mplot.axes.SubplotBase,
    background_color : str,
    plots : List[mplot.container.Container], # list of bar charts
    df : pd.DataFrame ):
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
      fname = "design/Montserrat_Medium.ttf",
      size = design.sizeText_legend ),
    facecolor = background_color,
    shadow=True,

    # The next arguments:
    # draw the legend to the right of the plot, ala
    # https://pythonspot.com/matplotlib-legend/
    loc = 'upper center',
    bbox_to_anchor = ( 1.45, 0.8 ),
    ncol = 1 )
  for text in leg.get_texts():
    text.set_color(
      design.against( background_color ) )

def add_outer_labels( ax : mplot.axes.SubplotBase,
                      xvals : np.ndarray,
                      units : str,
                      df : pd.DataFrame ):
  """Give vertical axis a label, no ticks, no tick labels. Based on
stackoverflow.com/questions/29988241/python-hide-ticks-but-show-tick-labels
"""
  ax.set_ylabel(
    units,
    color = design.orange,
    # PITFALL: If fontsize precedes fontproperties,
    # it gets clobbered.
    fontproperties = design.font_thin,
    fontsize = design.sizeText_tickLabel )

  plt.xticks( xvals,
              list( map( lambda s: int( float( s ) ),
                         df.columns ) ) )
  plt.setp( ax.get_xticklabels(),
            visible = True,
            color = 'k',
            fontproperties = design.font_thin )
  plt.setp( ax.get_yticklabels(), visible = False )
  ax.tick_params( axis='x', which='both', length=0 )
  ax.tick_params( axis='y', which='both', length=0 )
  ax.ticklabel_format( axis="y", style="plain" )
    # TRICKY: Even though the y-ticks are assigned `visible=False`,
    # a unit value for them (e.g. 1e10) will still appear
    # above the y-axis unless silenced by setting `style="plain"`
    # (`style` defaults to "scientific").
  for tick in ( ax.xaxis.get_major_ticks() +
                ax.yaxis.get_major_ticks() ):
      tick.label.set_fontsize( design.sizeText_tickLabel )
      tick.label.set_color( design.orange )
  ax.set_frame_on(False)

