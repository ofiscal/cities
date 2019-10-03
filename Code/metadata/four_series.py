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

series = [ingresos,gastos,ingresos-pct,gastos-pct]
series_dict = { "ingresos" : ingresos,
                "gastos"   : gastos,
                "ingresos-pct" : ingresos_pct,
                "gastos-pct" : gastos_pct }

