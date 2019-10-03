from Code.metadata.types import seriesType

ingresos = seriesType(
  name = "ingresos",
  peso_cols = ["item total"] ) # used to include "item recaudo" too
gastos = seriesType(
  name = "gastos",
  peso_cols = ["item oblig"] )

series = [ingresos,gastos]
series_dict = { "ingresos" : ingresos,
                "gastos"   : gastos }

