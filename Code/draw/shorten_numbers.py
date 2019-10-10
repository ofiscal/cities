import math as m

def commas( f: float ) -> int:
  """How many commas it would have, \
if it were printed in the United States style."""
  return ( 0 if abs(f) < 1
           else m.floor( m.log(abs(f)) / m.log(10) / 3))

if True: # test it
  assert commas(0.99) == 0
  assert commas(0.001) == 0
  assert commas(999) == 0
  assert commas(1001) == 1
  assert commas(1e6-1) == 1
  assert commas(1e6+1) == 2

def units( commas: int ) -> str:
  return ( { 0 : "2018 pesos",
             1 : "miles de 2018 pesos",
             2 : "millones de 2018 pesos",
             3 : "miles de millones de 2018 pesos",
             4 : "billones de 2018 pesos",
             5 : "miles de billones de 2018 pesos" } # absurdly big
           [commas] )
if True: # test it
  assert units( 0 )               == "2018 pesos"
  assert units( commas(123) )     == "2018 pesos"
  assert units( 2 )               == "millones de 2018 pesos"
  assert units( commas(1234567) ) == "millones de 2018 pesos"

def show_brief( f : float,
                  commas : int ) -> str:
  return ( "{0:.3g}" .
           format( f / 10**(3*commas) ) )
if True: # test it
  assert show_brief(9876,   1) == "9.88"
  assert show_brief(123456, 2) == "0.123"

