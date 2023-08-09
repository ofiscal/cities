from   typing import Set, List, Dict
from   os import path
import pandas as pd


sisfut_keys = "Code/explore/cuipo/concepto_keys/sisfut"

sg = pd.concat ( [
  ( pd.read_csv (
    path.join ( sisfut_keys,
                "inversion.csv" ) )
    [["observatorio name","item code","item"]] ),
  ( pd.read_csv (
    path.join ( sisfut_keys,
                "deuda.csv" ) )
    [["observatorio name","item code","item"]] ),
  ( pd.read_csv (
    path.join ( sisfut_keys,
                "funcionamiento.csv" ) )
    [["observatorio name","item code","item"]] ) ] )

sg.to_csv (
  path.join ( sisfut_keys,
              "gastos-collected.csv" ),
  index = False )
