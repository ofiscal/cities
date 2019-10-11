# This might be a better way to only overlay numbers on bars
# that offer enough room to do so.
room = ( # convert height from data coords to screen coords
  ax.transData.transform(( 0, height[cn] ))
  [1] )
if room > 120:

# This code can be used to print different things over the bars.
( abbrev.show_brief( bottom[cn], 3 ) + ", " +
  abbrev.show_brief( height[cn], 3 ) + ", " +
  abbrev.show_brief( top[cn], 3 ) ),
( abbrev.show_brief( bottom_in_pixels - floor, 0 ) + ", " +
  abbrev.show_brief( height_in_pixels - floor, 0 ) + ", " +
  abbrev.show_brief( top_in_pixels    - floor, 0 ) ),
( abbrev.show_brief( height[cn],       3 ) + " " +
  abbrev.show_brief( height_in_pixels, 0 ) ),

  # We might need the `floor` and (below) `relative_floor` variables
  # because the bottom of the chart is not at 0 pixels.
floor = ax.transData.transform(( 0, 0 ))[1]
relative_floor = floor if rn == 0 else 0

# Convert height from data coords to screen coords.
height_in_pixels = (
  ax.transData.transform(( 0, height[cn] ))
  [1] )
  # - relative_floor )
bottom_in_pixels = ( ax.transData.transform(( 0, bottom[cn] ))
                     [1] )
top_in_pixels = ( ax.transData.transform(( 0, top[cn] ))
                     [1] )

