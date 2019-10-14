if True:
  import pandas as pd
  import Code.build.classify_budget_codes as cla

cols = { "Cód. DANE Municipio"                      : "muni code",
         "Cód. DANE Departamento"                   : "dept code",
         "Código Concepto"                          : "item code",
         "Valor Total Pagado Vigencia Con Regalías" : "item oblig" }
  # PITFALL: "item oblig" isn't a name faithful to this file's raw data,
  # but it's consistent with the other gastos data downstream.

dfs_by_year = {}
for year in range(2013,2019):
  shuttle = (
    pd.read_excel(
      ( "data/gasto-con-regalias/gastoconregalias_" +
        str(year) + ".xlsx" ),
      usecols = list( cols.keys() ) ) .
    rename( columns = cols ) )
  shuttle = shuttle[
    shuttle["item code"] .
    isin( cla.of_interest["inversion"] ) ]
  shuttle["year"] = year
  dfs_by_year[year] = shuttle

tog = ( # all years together
  pd.concat( map( lambda year: dfs_by_year[year],
                  range(2013,2019 ) ) ) )

geo = ( tog[["muni code","year"]] . copy() .
        drop_duplicates() )
geo["one"] = 1
years_observed = ( geo . drop( columns = "year" ) .
                   groupby( "muni code" ) .
                   agg( sum ) .
                   sort_values( "one" ) )

def muni_sums_over_time( muni_code : int,
                       ) -> pd.Series:
  des = pd.DataFrame()
  for year in range(2013,2019):
    df = dfs_by_year[year]
    df = df[ df["muni code"] == muni_code ]
    year_mean = pd.Series( [df["item oblig"].sum()] )
    year_mean.name = year
    des = pd.concat(
      [des, year_mean],
      axis = "columns",
      sort = True ) # because initially des has no rows
  res = des.iloc[0]
  res.name = mc
  return res

long_observed = (
  years_observed[
    years_observed["one"] > 5 ] .
  reset_index() ) # we need the index to be a column too
long_observed.index = long_observed["muni code"]

all_muni_sums_over_time = (
  long_observed .
  apply( ( lambda row:
           muni_sums_over_time( row["muni code"] ) ),
         axis = "columns" ) )

# all_muni_sums_over_time.to_excel( "muni sums by year.xlsx" ) )

