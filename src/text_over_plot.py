# import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import numpy as np


plt.subplot(2, 1, 1)
with open ("data/text.txt", "r") as myfile:
    text = map( lambda s: s.replace( "\n","" )
              , myfile.readlines() )
# list(text)[0]
plt.text( 0, 0.5, "a\nb", verticalalignment="center" )
#        , transform="axes" )

plt.subplot(2, 1, 2)
x2 = np.linspace(0.0, 2.0)
y2 = np.cos(2 * np.pi * x2)
plt.plot(x2, y2, '.-')
plt.xlabel('time (s)')
plt.ylabel('displacement')

plt.show()
