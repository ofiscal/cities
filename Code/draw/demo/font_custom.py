# Based on: https://matplotlib.org/examples/api/font_file.html
# Ordinarily, reading a font from a fixed location is not recommended.
# However, in this case the font is part of the repo.
# It might be space-inefficient, but it's certainly safe.

import matplotlib.font_manager as fm


fig, ax = plt.subplots()
ax.plot([1, 2, 3])
font_black = "fonts/Montserrat_Black.ttf"
font_light = "fonts/Montserrat_Light.ttf"

ax.set_title(
    'Check out this custom font!'
  , fontproperties =
    fm.FontProperties(fname=font_black) )
ax.set_xlabel('This, by contrast, is the default font')

plt.show()

