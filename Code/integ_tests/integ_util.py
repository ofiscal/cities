if True:
  import numpy as np
  import pandas as pd
  from typing import List, Set, Dict

# pd.set_option('display.max_rows', 500)

if True: # 2014 is nice because it requires scaling by 1000 and deflation.
  # Muni ARACATACA and dept SANTANDER are nice because both include
  # multiple disaggregated observations of the same education code.
  # See integ_tests/raw.py for a proof.
  year = 2014        # was (ala sample_tables.py): 2018
  muni = "ARACATACA" # was (ala sample_tables.py): "SANTA MARTA"
  dept = "SANTANDER" # was (ala sample_tables.py): "ANTIOQUIA"

if True: # budget categories convenient for testing,
         # i.e. withthe fewest components
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
