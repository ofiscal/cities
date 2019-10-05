import pandas as pd
from math import (log,floor)


### Functions for hiding "comma places"
#
# To write 14,000 as 14 thousand is to suppress one comma place.
# To write 14,000,000 as 14 million is to suppress two comma places.
# Etc.

def shorter_numbers( df0 : pd.DataFrame ) -> (pd.DataFrame, str):
  df = df0.copy()
  commas = floor( log( df.max().max(),
                       1000 ) )
  words_for_comma_places = { 1 : "miles"
                           , 2 : "millones"
                           , 3 : "mil millones"
                           , 4 : "billones"
                           , 5 : "mil billones" }
  unit = words_for_comma_places[ commas ]
  return ( df / 1000**commas,
           unit)
if True: # test it
  x = pd.DataFrame( { "a" : [20e3,2e2],
                      "b" : [1,np.nan] } )
  y = pd.DataFrame( { "a" : [20,0.2],
                      "b" : [0.001,np.nan] } )
  assert shorter_numbers(x)[0].equals(y)
  assert shorter_numbers(x)[1] == "miles"
  x = pd.DataFrame( { "a" : [20e3,2e6],
                      "b" : [1,np.nan] } )
  y = pd.DataFrame( { "a" : [20e-3,2],
                      "b" : [1e-6,np.nan] } )
  assert shorter_numbers(x)[0].equals(y)
  assert shorter_numbers(x)[1] == "millones"
  del(x,y)

