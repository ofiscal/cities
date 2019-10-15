if True:
  from typing import List
  import Code.draw.chart.time_series as ts
  import Code.draw.chart.pairs as pairs

class chartPage:
  def __init__(self,file, insertNewlines, title, text, index_col, drawChart):
    self.file = file
    self.insertNewlines = insertNewlines
    self.title = title
    self.text = text
    self.index_col = index_col
    self.drawChart = drawChart

def page1( muni_short : str,
           dept_short : str ) -> chartPage:
  return chartPage(
    file = "ingresos-pct-compare",
    insertNewlines = True,
    title = ["¿De dónde viene la plata de " + muni_short,
             "y cómo se compara con el promedio de " + dept_short + "?"],
    text = ["Se muestra el acumulado de los ingresos de esta " +
            "administración (2015 a 2018) en cada sector."],
    index_col = 0,
    drawChart = pairs.drawPairs)
 
def page2( muni_short : str,
           dept_short : str ) -> chartPage:
  return chartPage(
    file = "gastos-pct-compare",
    insertNewlines = True,
    title = ["¿Cómo se gasta* la plata " + muni_short,
             "y cómo se compara con el promedio de " + dept_short + "?"],
    text = ["Se muestra el acumulado de los ingresos de esta" +
            "administración (2015 a 2018) en cada sector."],
    index_col = 0,
    drawChart = pairs.drawPairs)

def page3( muni_short : str ) ->  chartPage:
  return chartPage(
    file = "ingresos",
    insertNewlines = False,
    title = ["¿De dónde se obtuvo la plata de " + muni_short,
             "en esta administración y en la anterior?"],
    text = ["En el 2015 hubo cambio de gobierno municipal."],
    index_col = "item categ",
    drawChart = ts.drawStacks)

def page4( muni_short : str ) ->  chartPage:
  return chartPage(
    file = "gastos",
    insertNewlines =False,
    title = ["¿En qué se han gastado* la plata la alcaldía y el concejo",
              "de " + muni_short +"? ¿En qué se gastaron la plata la alcaldía",
              "y el concejo anteriores?"],
    text =  ["En el 2015 hubo cambio de gobierno municipal."],
    index_col = "item categ",
    drawChart = ts.drawStacks)

def pages( muni_short : str,
           dept_short : str ) -> List[chartPage]:
  return [page1(muni_short,dept_short),
          page2(muni_short,dept_short),
          page3(muni_short),
          page4(muni_short)]

