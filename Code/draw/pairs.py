# based on
# https://matplotlib.org/3.1.1/gallery/units/bar_unit_demo.html

if True:
  import matplotlib.pyplot as plt
  import numpy as np
  import pandas as pd
  #
  import Code.draw.newlines as newlines
  import matplotlib.ticker as ticker

if True: # read, tweak data
  df = pd.read_csv(
    ( "output/pivots/recip-100/CAUCA/TIMBIQUÍ/" +
      "gastos-pct-compare.csv" ),
    index_col = 0 )
  df.index = list( map( lambda s: newlines.remap[s],
                        df.index ) )

if True: # inputs to drawing functions
  muni = df.iloc[:,0]
  avg  = df.iloc[:,1]
  ind = np.arange(len(df)) # the x locations for the groups
  width = 0.35             # the width of the bars

if True: # draw
  fig, ax = plt.subplots()
  if True: # bars
    p0 = ax.bar(ind, muni, width, bottom=0)
    p1 = ax.bar(ind + width, avg, width, bottom=0)
  if True: # text
    ax.set_title('Title')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels( df.index,
                        fontsize = 7 )
    ax.yaxis.set_major_formatter(
      # https://stackoverflow.com/questions/31357611/format-y-axis-as-percent#comment68265158_35446404
      ticker.FuncFormatter('{0:.0%}'.format ) )

  ax.legend( (p0[0], p1[0]),
             (df.columns[0], df.columns[1]))
  plt.grid( True,
            axis="y",
            color="orange" )
  ax.autoscale_view()

plt.savefig( "output/a-city-comparison.png" )

