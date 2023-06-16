if True:
  import Code.metadata.terms as t
  from Code.metadata.types import seriesType

ingresos = seriesType(
  name = t.ingresos,
  money_cols = ["item total"] ) # PITFALL: used to include "item recaudo" too
ingresos_pct = seriesType(
  name = t.ingresos_pct,
  money_cols = ["item total"] )
gastos = seriesType(
  name = t.gastos,
  money_cols = ["item oblig"] )
gastos_pct = seriesType(
  name = t.gastos_pct,
  money_cols = ["item oblig"] )

series = [ ingresos,
           ingresos_pct,
           gastos,
           gastos_pct ]
series_dict = { t.ingresos     : ingresos,
                t.ingresos_pct : ingresos_pct,
                t.gastos       : gastos,
                t.gastos_pct   : gastos_pct }

series_pct = [ingresos_pct, gastos_pct]
