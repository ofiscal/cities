# import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager as fm
import datetime
import numpy as np


font_black = "fonts/Montserrat_Black.ttf"
font_light = "fonts/Montserrat_Light.ttf"

plt.subplot(2, 1, 1)
with open ("data/text.txt", "r") as myfile:
    text = map( lambda s: s.replace( "\n","" )
              , myfile.readlines() )
plt.text( 0, 0.5
        , "\n".join( text )
        , fontproperties =
          fm.FontProperties(fname=font_black)
        , verticalalignment="center" )
#        , transform="axes" )

plt.subplot(2, 1, 2)
x2 = np.linspace(0.0, 2.0)
y2 = np.cos(2 * np.pi * x2)
plt.plot(x2, y2, '.-')
plt.xlabel('time (s)')
plt.ylabel('displacement')

plt.show()
