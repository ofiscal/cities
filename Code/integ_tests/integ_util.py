if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict

subsample = 100

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)

if True: # define a spacetime cell
  if True: # This is the only dept with a "promedio" in the 1/1000 sample
    year = 2017
    muni = "VILLAPINZÓN"
    dept = "CUNDINAMARCA"
  if False: # VICHADA is nice because it only has 4 municipalities
    year = 2018
    muni = "CUMARIBO"
    dept = "VICHADA"
  if False: # values good for testing the pipeline
    # 2014 is nice because it requires scaling by 1000 and deflation.
    # Muni ARACATACA and dept SANTANDER are nice because both include
    # multiple disaggregated observations of the same education code.
    # See integ_tests/raw.py for a proof.
    year = 2014
    muni = "ARACATACA"
    dept = "SANTANDER"
  if False: # a subset of the values used in sample_tables.py
    year = 2018
    muni = "SANTA MARTA"
    dept = "ANTIOQUIA"
  if False:
    year = 2018
    muni = "BOGOTÁ, D.C."
    dept = "BOGOTÁ, D.C."

# muni code         muni  dept code       dept
#   47001.0  SANTA MARTA         47  MAGDALENA
#                         dept code       dept
#                                 5  ANTIOQUIA

if True: # budget categories convenient for testing,
         # i.e. with the fewest components
  if True: # results
    infra_codes = {'A.15', '1.3.11', 'A.7', 'A.9'}
    edu_codes = {'1.3.6.1.1', 'A.1', '1.3.6.4.1', '1.3.6.4.6'}
  if False: # research
    for k in codes.categs_to_code_sets.keys():
      print( "\n" + k + ": " +
             str( codes.categs_to_code_sets[k] ) )
    """ RESULT: Two good categories would be these:
    Infraestructura y vivienda: {'A.15', '1.3.11', 'A.7', 'A.9'}
    Educación: {'1.3.6.1.1', 'A.1', '1.3.6.4.1', '1.3.6.4.6'}
    One involves multiple inversion codes and one funcionamiento code,
    and the other the reverse. """

