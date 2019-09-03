# There are three series for each municipality:
# ingresos, inversion and funcionamiento.
# Each is drawn a little differently; this file specifies how.


class seriesType:
  def __init__(self, name, pesos_col):
    self.name = name
    self.pesos_col = pesos_col

ingresos = seriesType(
  name = "ingresos",
  pesos_col = "item recaudo" )
gastos = seriesType(
  name = "gastos",
  pesos_col = "item oblig" )

series = [ingresos,gastos]
series_dict = { "ingresos" : ingresos,
                "gastos"   : gastos }
