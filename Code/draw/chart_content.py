if True:
  from typing import List
  import Code.draw.chart.time_series as ts
  import Code.draw.chart.pairs as pairs
  import Code.draw.design as design

class chartPage:
  def __init__(self,
               file, background_color, insertNewlines,
               title, text, index_col, drawChart):
    self.file = file
    self.background_color = background_color
    self.insertNewlines = insertNewlines
    self.title = title
    self.text = text
    self.index_col = index_col
    self.drawChart = drawChart

def page1( muni_short : str,
           dept_short : str ) -> chartPage:
  return chartPage(
    file = "ingresos-pct-compare",
    background_color = "white",
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
    background_color = design.dark_blue,
    insertNewlines = True,
    title = ["¿Cómo se gasta* la plata " + muni_short,
             "y cómo se compara con el promedio de " + dept_short + "?"],
    text = ["Se muestra el acumulado de los ingresos de esta " +
            "administración (2015 a 2018) en cada sector."],
    index_col = 0,
    drawChart = pairs.drawPairs)

def page3( muni_short : str ) ->  chartPage:
  return chartPage(
    file = "ingresos",
    background_color = "white",
    insertNewlines = False,
    title = ["¿De dónde se obtuvo la plata de " + muni_short,
             "en esta administración y en la anterior?"],
    text = ["En el 2015 hubo cambio de gobierno municipal."],
    index_col = "item categ",
    drawChart = ts.drawStacks)

def page4( muni_short : str ) ->  chartPage:
  return chartPage(
    file = "gastos",
    background_color = design.dark_blue,
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

