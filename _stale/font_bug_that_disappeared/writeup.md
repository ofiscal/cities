Does font_manager have trouble reading underscores?

The make utility has trouble understanding hyphens, so I usually convert them to underscores in the files I'm working with. I took two fonts called "Black" and "Light" from the [Montserrat family](https://github.com/JulietaUla/Montserrat/tree/master/fonts/ttf), and discovered that if I change the hyphens in their names to underscores, Matplotlib treats "Light" as if it were "Black".

```
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fonts  = [
    # These two font files are identical
    "fonts/Montserrat_Black.ttf"
  , "fonts/Montserrat-Black.ttf"
  
    # These two font files are identical, and distinct from the previous two
  , "fonts/Montserrat_Light.ttf"
  , "fonts/Montserrat-Light.ttf"
  ]

for (i,f) in zip( [1,2,3,4], fonts ):
  plt.subplot(4, 1, i)
  plt.text( 0, 0.5
          , "A phrase to test the font"
          , fontproperties =
            fm.FontProperties(fname=f) )

plt.show()
```

I expected the first two lines to look the same (dark), and the second two lines to look the same (light), but in fact the first three all look the same (dar), and only the last one looks different (light).

I'm evaluating this code from a Jupyter notebook, so I precede it by first evaluating the line `%matplotlib inline`. It's all using Anaconda version 3.6.8.
