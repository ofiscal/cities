
# To give a title to a chart
ax.set_title( "Cool stuff",
              color = 'k',
              fontproperties = design.font_thick )

# Dunno. It was at the start of time_series.add_legend,
# but has no visible effect.
plt.rcParams['axes.titlepad'] = 10

ax.set_xlabel( "Year",
               color = 'k',
               fontproperties = design.font_thin )

