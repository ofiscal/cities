# Some data was made (by me) from .xlsx files through ssconvert.
# Other was made (by Juan) by running Save As in Excel.
# They're damn close -- with max disagreement of about 5e-9.

if True:
  import pandas as pd
  import Code.util as util

if True:
  juan = ( pd.read_csv( "regalias_municipios.csv", sep=";" ) .
           sort_values( ["cod_dane","nombre_mun","departamento"] ) )
  jeff = ( pd.read_csv( "data/regalias/muni.csv" ) .
           sort_values( ["cod_dane","nombre_mun","departamento"] ) )

for c in [ 'periodo 2019-2020',
           'periodo 2017-2018',
           'periodo 2016-2015',
           'periodo 2013-2014']:
  juan[c] = juan[c].str.replace(".","")
  jeff = util.un_latin_decimal_columns( [c], jeff )
  juan = util.un_latin_decimal_columns( [c], juan )

for c in jeff.columns:
  print( c,   juan[c].equals(jeff[c]) )

x = pd.concat( [ jeff["periodo 2019-2020"],
                 juan["periodo 2019-2020"] ],
               axis = "columns" )

(x.iloc[:,0] - x.iloc[:,1]).max()

