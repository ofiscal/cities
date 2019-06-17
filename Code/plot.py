import matplotlib.pyplot as plt
from   matplotlib.backends.backend_pdf import PdfPages
import Code.lib as lib


plt.rcParams['axes.facecolor'] = 'b'

with PdfPages('output/a page.pdf') as pdf:
  lib.drawPage( "data" )
  pdf.savefig( facecolor=lib.background_color )
  plt.close()
