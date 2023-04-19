if True:
  import Code.metadata.terms as t
  from Code.metadata.types import seriesType

ingresos = seriesType(
  name = t.ingresos,
  money_cols = ["item total"] ) # used to include "item recaudo" too
gastos = seriesType(
  name = t.gastos,
  money_cols = ["item oblig"] )

series = [ingresos,gastos]
series_dict = { t.ingresos : ingresos,
                t.gastos   : gastos }
