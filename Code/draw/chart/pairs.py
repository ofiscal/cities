# based on
# https://matplotlib.org/3.1.1/gallery/units/bar_unit_demo.html

if True:
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib.font_manager as fm
  import numpy as np
  import pandas as pd

  import Code.draw.design               as design
  import Code.draw.text.newlines        as newlines
  import Code.draw.text.shorten_numbers as abbrev
  import Code.draw.text.shorten_names as shorten_names

def drawPairs( ax : mplot.axes.SubplotBase,
               background_color : str,
               df : pd.DataFrame ):

  # The muni is in the first column, and the dept average in the second.
  muni_col = 0
  avg_col = 1
  totals = df.sum()

  if True: # definitions
    muni = df.iloc[:,muni_col]
    avg  = df.iloc[:,avg_col]
    ind = np.arange(len(df))    # the x locations for the groups
    width = design.sizeBarWidth # the width of the bars

  if True: # bars
    p0 = ax.bar(ind, muni, width, bottom=0)
    p1 = ax.bar(ind + width, avg, width, bottom=0)

  for (geo, x_shift) in [ # plot totals above each column
      (muni_col, 0),
      (avg_col, width) ]:
    for budget in range(len(df)):
      y_shift = ( # Convert 0.04 from axes coords to screen coords,
                  # and then from screen coords to data coords.
        ax.transData.inverted().transform(
          ax.transAxes.transform( (0,0.04) ) )
        [1] )
      ax.text( budget + x_shift,
               df.iloc[budget,geo] + y_shift,
               ( abbrev.show_brief( # what we're printing
                   100 * df.iloc[budget,geo] / totals[geo],
                   0 )
                 + "%"),
               verticalalignment = 'center',
               horizontalalignment = 'center',
               color = design.against( background_color ),
               fontproperties = design.font_thin,
               fontsize = design.sizeText_aboveBars )

  if True: # grid (and grid text)
    ax.set_axisbelow(True) # to keep grid lines behind bars
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels( df.index )
    for tick in ( ax.xaxis.get_major_ticks() +
                  ax.yaxis.get_major_ticks() ):
      tick.label.set_fontsize( design.sizeText_tickLabel )
      tick.label.set_color( design.orange )
    ax.yaxis.set_major_formatter(
      # https://stackoverflow.com/questions/31357611/format-y-axis-as-percent#comment68265158_35446404
      ticker.FuncFormatter('{0:.0%}'.format ) )
    plt.grid( True, # add horizontal lines
              axis="y",
              linewidth = design.sizeLineWidth,
              color = design.orange )
  
  leg = ax.legend(
    (p0[0], p1[0]),
    ( shorten_names.munis[df.columns[0]] . upper(),
      df.columns[1] ),
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
    shadow=True )
  for text in leg.get_texts():
    text.set_color(
      design.against( background_color ) )

  ax.set_frame_on(False)
  ax.autoscale_view()


testing = False
if testing:
  df = pd.read_csv(
    ( "output/pivots/recip-100/CAUCA/TIMBIQUÍ/" +
      "gastos-pct-compare.csv" ),
    index_col = 0 )
  df.index = list( map( lambda s: newlines.remap[s],
                        df.index ) )
  fig, ax = plt.subplots()
  drawPairs( ax, df )
  plt.savefig( "output/a-city-comparison.png" )

