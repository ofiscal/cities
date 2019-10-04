# matplotlib: Use (the same) custom font in every kind of text: axes, title, text overlays, legend ...

I am drawing a plot, and I need to use a particular custom font everywhere in it. I've discovered how to use a custom font when using `matplotlib.pyplot.text`:

```
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd

font_black = "fonts/Montserrat_Black.ttf" # A local file
font_light = "fonts/Montserrat_Light.ttf" # Another local file

plt.text( 0.5, 0.5, "Wuz hatnen?"
        , fontproperties =
          fm.FontProperties(fname=font_black) )
plt.show()
```

But I need to use that font in many other kinds of text -- the title, the axis labels, the tick labels, the legend, and the text drawn via `Axes.text`. I'm hoping there's a global control that changes the font used for everything in the plot. I was hopeful about `matplotlilb.pyplot.rc`, but couldn't get it to work. I also tried using individual text-setting functions like `Axes.set_title` (rather than the more general `Axes.set`) but couldn't get that to work either.

The following demonstrates all the kinds of things I'm drawing; it works, but doesn't do the fonts.

```
df = pd.DataFrame( { "2014": [1,2,3,4]
                   , "2015": [3,4,5,1] }
                 , index=["Saturn","hedgehog","abstract","crunk"] )

_,ax = plt.subplots()
nCols = len( df.columns )
nRows = len( df.index )
xvals = np.arange( nCols )

if True: # Draw stuff.
  plots = {}
  for rn in range(nRows):

    if True: # Irrelevant details -- stack some box plots.
      if rn < 1: bottom = [0. for i in range(nCols)]
      else:      bottom = df.iloc[0:rn,:].sum()
      top =      bottom + df.iloc[  rn,:]
      plots[rn] = ax.bar(
          xvals
        , df.iloc[rn,:]
        , width = [ 0.8 for i in range( nCols ) ]
        , bottom = bottom )

    for cn in range( nCols ): # Overlay text onto the box plot boxes
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

plt.show()
```
