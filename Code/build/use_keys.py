if True:
  import os.path as path
  import pandas as pd
  #
  import Code.common as common


if True: # get, test data
  geo = (
    pd.read_csv ( path.join ( common.outdata, "keys",
                              "geo.csv" ) ) .
    rename ( columns =
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

if True: # how to add a column that counts munis in each dept
  def add_munis_in_dept_col(
      df : pd.DataFrame ) -> pd.DataFrame:
    """ Adds a column indicating how many munis are in each dept. """
    new = ( df[df["muni code"]!=0]
              [["dept code"]] )
    new["muni count"] = 1
    new = ( new . groupby(["dept code"]) .
            agg({"dept code" : "first",
                 "muni count"     : sum}) .
            reset_index(drop=True) )
    return df.merge( new, how="left", on="dept code" )
  if True: # test it
    x = pd.DataFrame( { "dept code"  : [1,11,11,22,22,22,22],
                        "muni code"  : [1,2,3,4,5,6, 0],
                        "noise"      : [1,2,3,4,5,6,7] } )
    y = add_munis_in_dept_col(x)
    z = pd.DataFrame( { "dept code"  : [1,11,11,22,22,22,22],
                        "muni code"  : [1,2,3,4,5,6, 0],
                        "noise"      : [1,2,3,4,5,6,7],
                        "muni count" : [1,2,2,3,3,3,3] } )
    assert y.equals(z)

if True:
  depts_and_munis = (
    pd.concat(
      [depts,geo],
      axis = "rows",
      sort = True ) ) # because depts.columns != munis.columns
  depts_and_munis["muni"] = (
    depts_and_munis["muni"].fillna("dept") )
  depts_and_munis["muni code"] = (
    depts_and_munis["muni code"].fillna(0) )
  depts_and_munis = add_munis_in_dept_col(
    depts_and_munis )
  depts_and_munis = (
    # For Bogotá the muni info is equal to the dept info,
    # so including a dept observation would be redundant.
    depts_and_munis[
      ~ ( ( depts_and_munis["dept"] == "BOGOTÁ, D.C." ) &
          ( depts_and_munis["muni"] == "dept" ) ) ] )

def merge_geo( df : pd.DataFrame ) -> pd.DataFrame:
  # Left-merge because we're only trying to add information to df,
  # and munis or depts might contain places not in df.
  return (
    df .
    merge( munis,
           how = "left",
           on = ["muni code"] ) .
    merge( depts,
           how = "left",
           on = ["dept code"] ) )
