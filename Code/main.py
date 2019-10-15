if True:
  from typing import List, Set, Dict
  from   pathlib import Path
  import pandas as pd
  from   matplotlib.backends.backend_pdf import PdfPages
  #
  import Code.common as c
  import Code.metadata.four_series as s4
  import Code.build.use_keys as uk
  import Code.draw.pages as pages
  import Code.draw.text.shorten_names as shorten_names
  import Code.draw.text.newlines as newlines
  import Code.draw.chart_content as chart_content


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
