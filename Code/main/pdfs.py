if True:
  from   typing import List, Set, Dict
  from   pathlib import Path
  import pandas as pd
  from   matplotlib.backends.backend_pdf import PdfPages
  #
  import Code.common as c
  import Code.metadata.four_series as s4
  import Code.draw.pages as pages
  import Code.draw.text.shorten_names as shorten_names
  import Code.draw.text.newlines as newlines
  import Code.draw.chart_content as chart_content
  from   Code.main.geo import geo

def create_pdf( dept : str,
                muni : str ):
  folder = ( root + "/" + dept + "/" + muni )
  print("folder: ", folder)

  muni_short = shorten_names.munis[muni]
  dept_short = shorten_names.depts[dept]
  muni_split = (
    shorten_names.split_at_middlest_space(
      muni_short)
    if len(muni_short) > 15
    else muni_short )

  with PdfPages( folder + "/report.pdf" ) as pdf:
    pages.drawTitlePage( muni_split, pdf )
    for page in chart_content.pages( muni_short, dept_short):
      df = pd.read_csv(
        folder + "/" + page.file + ".csv",
        index_col = page.index_col )
      if page.insertNewlines:
        df.index = list( map( lambda s: newlines.remap[s],
                              df.index ) )
      pages.drawPageWithChart(
        df, page.background_color, page.title, page.text, pdf, page.drawChart )
    pages.drawZenQuestions( muni_short, pdf )
    pages.drawLastPage( pdf )

root = "output/pivots/recip-" + str(c.subsample)

geo.apply(
  ( lambda row:
    create_pdf( dept = row["dept"],
                muni = row["muni"] ) ),
  axis = "columns" )

( Path( root + "/" + "timestamp-for-pdfs" ) .
  touch() )

