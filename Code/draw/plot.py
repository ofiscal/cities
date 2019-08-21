import pandas as pd
import matplotlib.pyplot as plt
from   matplotlib.backends.backend_pdf import PdfPages

import Code.draw.lib as lib


plt.rcParams['axes.facecolor'] = 'b'

if True: # define df, title, text
  folder = "data/example/"
  df = pd.read_csv( folder + "numbers_to_plot.csv"
                  , index_col=0 )
  with open( folder + "/title.txt", "r") as myfile:
      title = myfile.readlines()
  with open( folder + "/text.txt", "r") as myfile:
      text = myfile.readlines()
  del(folder)

with PdfPages('output/a_page.pdf') as pdf:
  lib.drawPage( df, title, text )
  pdf.savefig( facecolor=lib.background_color )
  plt.close()

