if True:
  import os
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
  from   Code.main.geo import depts_and_munis

# Use this if in a hurry and only in need of the
# facebook-treated group.
# treated = pd.read_excel( "data/regions/fb-treated.xlsx" )
# treated_muni_set = set( treated["muni code"] )

source_root = "output/pivots/recip-"  + str(c.subsample)
dest_folder = "output/reports/recip-" + str(c.subsample)

def create_pdf( dept : str,
                muni : str,
                muni_code : int ):

  # Use one of these if in a hurry or not in need of all data.
  #
  # if ( (c.subsample == 1) &
  #      ~(muni_code in treated_muni_set) ): return
  #
  # if not ( int(muni_code) in [ 15332,     # Güicán
  #                              50370 ] ): # (La) Uribe
  #       return

  if True: # folders
    source = ( source_root + "/" + dept + "/" + muni )
    if not os.path.exists( dest_folder ):
      os.makedirs( dest_folder )
    print("folder: ", source)

  muni_short = shorten_names.munis[muni]
  dept_short = shorten_names.depts[dept]
  muni_split = (
    shorten_names.split_at_middlest_space(
      muni_short)
    if len(muni_short) > 15
    else muni_short )
  dest_file = dest_folder + "/" + str(muni_code) + ".pdf"

  with PdfPages( dest_file ) as pdf:
    pages.drawTitlePage( muni_split, pdf )
    for page in chart_content.pages( muni_short, dept_short):
      df = pd.read_csv(
        source + "/" + page.file + ".csv",
        index_col = page.index_col )
      if page.insertNewlines:
        df.index = list( map( lambda s: newlines.remap[s],
                              df.index ) )
      pages.drawPageWithChart(
        df, page.background_color, page.title, page.text,
        pdf, page.drawChart )
    pages.drawZenQuestions( muni_short, pdf )
    pages.drawLastPage( pdf )

( depts_and_munis .
  sort_values( "muni code" ) .
  apply(
  ( lambda row:
    create_pdf( dept      =      row["dept"],
                muni      =      row["muni"],
                muni_code = int( row["muni code"] ) ) ),
  axis = "columns" ) )

( Path( dest_folder + "/" + "timestamp-for-reports" ) .
  touch() )

