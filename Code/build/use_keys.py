if True:
  import os
  import numpy as np
  import pandas as pd
  #
  import Code.common as c
  import Code.util.misc as util
  import Code.metadata.two_series as ser


if True: # get, test data
  geo = (
    pd.read_csv( "output/keys/geo.csv" ) .
    rename( columns =
            { "Cód. DANE Municipio"      : "muni code",
              "Cód. DANE Departamento"   : "dept code",
              "Nombre DANE Municipio"    : "muni",
              "Nombre DANE Departamento" : "dept" } ) )
  depts = ( geo[["dept code","dept"]] .
            groupby( "dept code" ) .
            agg('first') .
            reset_index() )
  assert depts.shape == (33,2)
  assert pd.isnull(depts).any().any() == False
  munis = geo[["muni code","muni"]]
  assert munis.shape == (1101,2)
  assert pd.isnull(munis).any().any() == False

if True:
  depts_and_munis = (
    pd.concat(
      [depts,geo],
      axis = "rows",
      sort = True ) ) # because depts.columns != munis.columns
  depts_and_munis["muni"] = (
    depts_and_munis["muni"].fillna("dept") )
  depts_and_munis["muni code"] = (
    depts_and_munis["muni"].fillna(-1) )
  depts_and_munis = (
    # For Bogotá the muni info is equal to the dept info,
    # so including a dept observation would be redundant.
    depts_and_munis[
      ~ ( ( depts_and_munis["dept"] == "BOGOTÁ, D.C." ) &
          ( depts_and_munis["muni"] == "dept" ) ) ] )

def merge_geo( df : pd.DataFrame ) -> pd.DataFrame:
  return (
    df .
    merge( munis,
           how = "left", # b/c muni code is can be missing (for dept data)
           on = ["muni code"] ) .
    merge( depts,
           how = "left", # this is unnecessarily cautious,
                         # as dept is never missing
           on = ["dept code"] ) )

