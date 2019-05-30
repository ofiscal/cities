import sys
import os
import matplotlib.font_manager as fm


fig, ax = plt.subplots()
ax.plot([1, 2, 3])
font_black = "fonts/Montserrat-Black.ttf"
font_light = "fonts/Montserrat-Light.ttf"

ax.set_title(
    'Check out this font!'
  , fontproperties =
    fm.FontProperties(fname=font_black) )
ax.set_xlabel('This is the default font')

plt.show()
