if True:
  from typing import List, Set, Dict
  from   pathlib import Path
  import pandas as pd
  from   matplotlib.backends.backend_pdf import PdfPages
  #
  import Code.common as c
  import Code.metadata.four_series as s4
  import Code.build.use_keys as uk
  import Code.draw.chart.time_series as ts
  import Code.draw.chart.pairs as pairs
  import Code.draw.pages as pages
  import Code.draw.text.shorten_names as shorten_names
  import Code.draw.text.newlines as newlines


def create_pdf( dept : str,
                muni : str ):
  folder = ( root + "/" + dept + "/" + muni )
  muni_short = shorten_names.munis[muni]
  dept_short = shorten_names.depts[dept]
  print("folder: ", folder)

  with PdfPages( folder + "/report.pdf" ) as pdf:
    pages.drawTitlePage( muni_short, pdf )
    for  (file, insertNewlines, title, text, index_col, drawChart) in [
         ( "ingresos-pct-compare", True,
           ["¿De dónde viene la plata de " + muni_short,
            "y cómo se compara con el promedio de " + dept_short + "?"],
           ["Se muestra el acumulado de los ingresos de esta" +
            "administración (2015 a 2018) en cada sector."],
           0,            pairs.drawPairs),
         ( "gastos-pct-compare",   True,
           ["¿Cómo se gasta* la plata " + muni_short,
            "y cómo se compara con el promedio de " + dept_short + "?"],
           ["Se muestra el acumulado de los ingresos de esta" +
            "administración (2015 a 2018) en cada sector."],
           0,            pairs.drawPairs),
         ( "ingresos",             False,
           ["¿De dónde se obtuvo la plata de " + muni_short,
            "en esta administración y en la anterior?"],
           ["En el 2015 hubo cambio de gobierno municipal."],
           "item categ", ts.drawStacks),
         ( "gastos",               False,
           ["¿En qué se han gastado* la plata la alcaldía y el concejo",
            "de " + muni_short +"? ¿En qué se gastaron la plata la alcaldía",
            "y el concejo anteriores?"],
           ["En el 2015 hubo cambio de gobierno municipal."],
           "item categ", ts.drawStacks) ]:
      df = pd.read_csv(
        folder + "/" + file + ".csv",
        index_col = index_col )
      if insertNewlines:
        df.index = list( map( lambda s: newlines.remap[s],
                              df.index ) )
      pages.drawPageWithChart(
        df, title, text, pdf, drawChart )
    pages.drawZenQuestions( muni_short, pdf )

root = "output/pivots/recip-" + str(c.subsample)

if True: # create geo indices to loop over
  geo = uk.merge_geo( # Using stage 6p7 rather than 7 because
    pd.read_csv(      # they are equivalent and it's smaller
      ( "output/budget_6p7_avg_muni/recip-" + str(c.subsample) +
        "/" + "gastos-pct.csv" ),
      usecols = ['dept code', 'muni code'] ) .
    drop_duplicates() .
    reset_index( drop=True ) .
    sort_values( ["dept code","muni code"] ) )
  geo = geo[ geo["muni code"] > 0 ]
  # geo.loc[ geo["muni code"]==0,
  #          "muni" ] = "dept"
  # geo.loc[ geo["muni code"]==-2,
  #          "muni" ] = "promedio"

geo.apply(
  ( lambda row:
    create_pdf( dept = row["dept"],
                muni = row["muni"] ) ),
  axis = "columns" )

( Path( root + "/" + "timestamp-for-pdfs" ) .
  touch() )

