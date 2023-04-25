# PITFALL: This program is redundant; it differs from
# reports.py in exactly one line, the one that defines
# which pages to loop over. This only loops over one of them.
# (The line reads `for page in [chart_content.page2 ...`.)

if True:
  from   matplotlib.backends.backend_pdf import PdfPages
  import matplotlib.pyplot as plt
  import os
  import pandas as pd
  from   pathlib import Path
  from   typing import List, Set, Dict
  #
  import Code.common as c
  import Code.draw.chart_content as chart_content
  import Code.draw.design as design
  import Code.draw.pages as pages
  import Code.draw.text.newlines as newlines
  import Code.draw.text.shorten_names as shorten_names
  from   Code.main.geo import depts_and_munis
  import Code.metadata.four_series as s4


source_root = os.path.join ( c.outdata, "pivots",
                             "recip-" + str(c.subsample) )
dest_folder = os.path.join ( c.outdata, "facebook_ads",
                             "recip-" + str(c.subsample) )

def create_pdf( dept : str,
                muni : str,
                muni_code : int ):
  muni_short = shorten_names.munis[muni]
  dept_short = shorten_names.depts[dept]
  if True: # folders
    source = ( source_root + "/" + dept + "/" + muni )
    if not os.path.exists( dest_folder ):
      os.makedirs( dest_folder )
    dest_file = ( ( dest_folder + "/"
                   + str(muni_code) + ".png" ) .
                  replace( " ", "-" ) )
    print("folder: ", source)
  page = chart_content.page2( muni_short, dept_short)
  df = pd.read_csv(
    source + "/" + page.file + ".csv",
    index_col = page.index_col )
  if page.insertNewlines:
    df.index = list( map( lambda s: newlines.remap[s],
                          df.index ) )
  if True:
    pages.set_page_size()
    pages.drawPageWithChart(
      df, page.background_color, page.title, page.text,
      None, # PITFALL: Setting pdf=None requires the user to save
            # and close the figure outside of this function call.
      page.drawChart )
  plt.savefig( dest_file,
               facecolor = design.dark_blue )
  plt.close()

depts_and_munis.apply(
  ( lambda row:
    create_pdf( dept      =      row["dept"],
                muni      =      row["muni"],
                muni_code = int( row["muni code"] ) ) ),
  axis = "columns" )

( Path( dest_folder + "/" + "timestamp-for-facebook-ads" ) .
  touch() )
