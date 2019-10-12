Matplotlib: inconsistent coordinate transformation

I'm plotting some stacked bar charts (see figure below). The top of each bar should be in the same place as the bottom of the bar stacked immediately on top of it. This is true if I measure them in data coordinates. However, if I translate those data coordinates to axes coordinates, it stops being true.

Consider the first (blue, bottom-left) bar in the figure. Measured in data, it has a bottom of 0, a height of 3, and a top of 3. (The text written on it states those measurements.) Great. And measured in axes, it has a bottom of 0, a height of 0.952, and a top of 0.952.

Now consider the orange bar immediately above it. In data, that bar has a bottom of 3 -- just like the top of the bar it's sitting on. But if I translate to axes coordinates, it has a bottom of 0.571, whereas the first (blue) bar it has a top of 0.952. Those two numbers should be equal but they are not.

This is weird, because in both cases I'm supplying the same input -- 3 -- to the transformation from data to axes coordinates.

The code uses only two commands to draw: `ax.bar`, to draw the bars, and `ax.text`, to draw the text over each bar. To transform from data to axes, I first transform from data to screen coordinates, and then from screen to axes; see the `transform` commands in the code for details.
