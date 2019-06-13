import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import code.lib as lib


df = pd.read_csv( "data/data.csv", index_col=0 )

with open ("data/text.txt", "r") as myfile:
    text = map( lambda s: s.replace( "\n","" )
              , myfile.readlines() )

lib.drawStacks( df )

plt.show()
