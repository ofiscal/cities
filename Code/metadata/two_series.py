# There are three series for each municipality:
# ingresos, inversion and funcionamiento.
# Each is drawn a little differently; this file specifies how.


class seriesType:
  def __init__(self, name, peso_cols):
    self.name = name
    self.peso_cols = peso_cols

ingresos = seriesType(
  name = "ingresos",
  peso_cols = ["item total"] ) # used to include "item recaudo" too
gastos = seriesType(
  name = "gastos",
  peso_cols = ["item oblig"] )

series = [ingresos,gastos]
series_dict = { "ingresos" : ingresos,
                "gastos"   : gastos }

