# based on
# https://matplotlib.org/3.1.1/gallery/units/bar_unit_demo.html

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv(
  ( "output/pivots/recip-100/CAUCA/TIMBIQUÍ/" +
    "gastos-pct-compare.csv" ),
  index_col = 0 )

muni = df.iloc[:,0]
avg  = df.iloc[:,1]
ind = np.arange(len(df)) # the x locations for the groups
width = 0.35             # the width of the bars

fig, ax = plt.subplots()

p0 = ax.bar(ind, muni, width, bottom=0)
p1 = ax.bar(ind + width, avg, width, bottom=0)

ax.set_title('Title')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(df.index)

ax.legend( (p0[0], p1[0]),
           (df.columns[0], df.columns[1]))
ax.autoscale_view()

plt.savefig( "output/a-city-comparison.png" )

