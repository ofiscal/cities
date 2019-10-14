# based on
# https://matplotlib.org/3.1.1/gallery/units/bar_unit_demo.html

import numpy as np
import matplotlib.pyplot as plt


N = 5
menMeans = (150, 160, 146, 172, 155)
womenMeans = (145, 149, 172, 165, 200)
ind = np.arange(N)    # the x locations for the groups
width = 0.35         # the width of the bars

fig, ax = plt.subplots()

p1 = ax.bar(ind, menMeans, width, bottom=0)
p2 = ax.bar(ind + width, womenMeans, width, bottom=0)

ax.set_title('Scores by group and gender')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

ax.legend((p1[0], p2[0]), ('Men', 'Women'))
ax.autoscale_view()

plt.savefig( "output/pairs-demo.png" )

