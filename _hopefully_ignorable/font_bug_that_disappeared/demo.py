import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fonts  = [
    # These two font files are identical
    "fonts/Montserrat_Black.ttf"
  , "fonts/Montserrat-Black.ttf"
  
    # These two font files are identical, and distinct from the previous two
  , "fonts/Montserrat_Light.ttf"
  , "fonts/Montserrat-Light.ttf"
  ]

for (i,f) in zip( [1,2,3,4], fonts ):
  plt.subplot(4, 1, i)
  plt.text( 0, 0.5
          , "A phrase to test the font"
          , fontproperties =
            fm.FontProperties(fname=f) )

# I expected the first two plots to look identical, and the last two,
# and the first two to look different from the last two.
# In fact the first three look identical, and only the last looks different.
plt.show()
