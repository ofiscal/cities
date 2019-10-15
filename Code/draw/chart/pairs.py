# based on
# https://matplotlib.org/3.1.1/gallery/units/bar_unit_demo.html

if True:
  import matplotlib as mplot
  import matplotlib.pyplot as plt
  import matplotlib.ticker as ticker
  import matplotlib.font_manager as fm
  import numpy as np
  import pandas as pd

  import Code.draw.text.newlines as newlines
  import Code.draw.design as design

def drawPairs( ax : mplot.axes.SubplotBase,
               background_color : str,
               df : pd.DataFrame ):

  if True: # definitions
    muni = df.iloc[:,0]
    avg  = df.iloc[:,1]
    ind = np.arange(len(df)) # the x locations for the groups
    width = 0.2              # the width of the bars
  
  if True: # bars
    p0 = ax.bar(ind, muni, width, bottom=0)
    p1 = ax.bar(ind + width, avg, width, bottom=0)

  if True: # grid (and grid text)
    ax.set_axisbelow(True) # to keep grid lines behind bars
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels( df.index )
    for tick in ( ax.xaxis.get_major_ticks() +
                  ax.yaxis.get_major_ticks() ):
      tick.label.set_fontsize( design.sizeText_tickLabel )
    ax.yaxis.set_major_formatter(
      # https://stackoverflow.com/questions/31357611/format-y-axis-as-percent#comment68265158_35446404
      ticker.FuncFormatter('{0:.0%}'.format ) )
    plt.grid( True, # add horizontal lines
              axis="y",
              linewidth = design.sizeLineWidth,
              color = design.orange )
  
  ax.legend(
    (p0[0], p1[0]),
    (df.columns[0], df.columns[1]),
    prop = fm.FontProperties( # PITFALL: This cannot be simplified.
        # Incredibly, if we first define
        #     def font_light_func( size : int ):
        #       fm.FontProperties( fname = "fonts/Montserrat_Light.ttf",
        #                          size = size )
        # and then replace the above `prop = fm.FontProperties(...)` call
        # with `prop = font_light_func(6)`, it behaves differently,
        # in particular using a huge font size.
      fname = "design/Montserrat_Light.ttf",
      size = design.sizeText_legend ),
    facecolor = background_color,
    shadow=True )

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

