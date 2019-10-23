# PYTHONPATH='.' python3 Code/main/html_wrappers.py

if True:
  import os
  import pandas as pd
  from   pathlib import Path
  import Code.common as c
  import Code.draw.text.shorten_numbers as abbrev
  import Code.metadata.terms as t
  from   Code.main.geo import depts_and_munis

# Use this if only in need of the facebook-treated group.
treated = pd.read_excel( "data/regions/fb-treated.xlsx" )
treated_muni_set = set( treated["muni code"] )

dest = "output/html/recip-" + str(c.subsample)
if not os.path.exists( dest ):
  os.makedirs( dest )

def write_html( muni_code : int ):
  """HTML lifted from https://www.codexworld.com/embed-pdf-document-file-in-html-web-page/"""
  if not muni_code in treated_muni_set: return
  dest_file = dest + "/" + str(muni_code) + ".html"
  with open( dest_file, "w" ) as f:
    f.write( """<embed src="http://www.luiscarlosreyes.com/wp-content/uploads/2019/10/""" + str(muni_code) + """.pdf" type="application/pdf" width="100%" height="100%" />""" )

( depts_and_munis["muni code"] .
  astype( int ) .
  apply( write_html ) )

( Path( dest + "/" + "timestamp-for-html" ) .
  touch() )

