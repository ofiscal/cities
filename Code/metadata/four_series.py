from Code.metadata.types import seriesType

ingresos = seriesType(
  name = "ingresos",
  money_cols = ["item total"] ) # PITFALL: used to include "item recaudo" too
ingresos_pct = seriesType(
  name = "ingresos-pct",
  money_cols = ["item total"] )
gastos = seriesType(
  name = "gastos",
  money_cols = ["item oblig"] )
gastos_pct = seriesType(
  name = "gastos-pct",
  money_cols = ["item oblig"] )

series = [ingresos,ingresos_pct,gastos,gastos_pct]
series_dict = { "ingresos" : ingresos,
                "ingresos-pct" : ingresos_pct,
                "gastos"   : gastos,
                "gastos-pct" : gastos_pct }

