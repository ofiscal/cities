if True:
  import pandas as pd
  import Code.build.classify_budget_codes as cla
  import matplotlib.pyplot as plt


######
###### Get gastos-from-regalias data
######

cols = { "Cód. DANE Municipio"                      : "muni code",
         "Cód. DANE Departamento"                   : "dept code",
         "Código Concepto"                          : "item code",
         "Valor Total Pagado Vigencia Con Regalías" : "item oblig" }
  # PITFALL: "item oblig" isn't a name faithful to this file's raw data,
  # but it's consistent with the other gastos data downstream.

regal_gastos_by_year = {}
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
  regal_gastos_by_year[year] = shuttle

del(shuttle, cols)

regal_gastos = ( # all years together
  pd.concat( map( lambda year: regal_gastos_by_year[year],
                  range(2013,2019 ) ) ) )

def regal_gastos_sum ( muni_code : int,
                       year : int ) -> float:
  df = regal_gastos[ (regal_gastos["muni code"] == muni_code) &
                   (regal_gastos["year"]      == year) ]
  return df["item oblig"].sum()

mc = 68377
yr = 2013
regal_gastos_sum(mc,yr)


######
###### Muni-year indices, and how many years a muni is observed
######

spacetime = ( regal_gastos[["muni code","year"]] . copy() .
              drop_duplicates() )
spacetime = spacetime[ ~pd.isnull(spacetime["muni code"])]

spacetime_redundant = spacetime.copy()
spacetime_redundant["mc"] = spacetime["muni code"]
spacetime_redundant["yr"] = spacetime["year"]

spacetime["one"] = 1
years_observed = ( spacetime . drop( columns = "year" ) .
                   groupby( "muni code" ) .
                   agg( sum ) .
                   sort_values( "one" ) )
spacetime = spacetime.drop( columns = "one" )


######
###### Ratio of regalias gastos to other gastos
######

ordin_gastos = pd.read_csv(
  "output/budget_7_verbose/recip-1/gastos.csv" )
ordin_gastos = ordin_gastos[
  ordin_gastos["muni code"] > 0 ]
total_ordin_gastos = (
  ordin_gastos[['muni', 'muni code', 'year', 'item oblig']] .
  groupby( ['muni', 'muni code', 'year'] ) .
  agg( sum ) . reset_index() )

def get_total_ordin_gastos( muni_code : int,
                            year : int ) -> float:
  return float(
    total_ordin_gastos
    [ (total_ordin_gastos["muni code"] == muni_code) &
      (total_ordin_gastos["year"] == year) ]
    ["item oblig"] )

def regal_to_other_spending( muni_code : int,
                             year : int ) -> float:
  return ( regal_gastos_sum(       muni_code, year ) /
           get_total_ordin_gastos( muni_code, year) )

mc = 68377
yr = 2013
( ordin_gastos
  [ (ordin_gastos["muni code"] == mc) &
    (ordin_gastos["year"] == yr) ]
  ["item oblig"] ) . sum()
get_total_ordin_gastos( mc, yr )
regal_to_other_spending( mc, yr )

ratios_regal_to_other_spending = (
  spacetime_redundant .
  groupby( ["muni code","year"] ) .
  apply( lambda row:
         regal_to_other_spending( row["mc"].iloc[0],
                                row["yr"].iloc[0] ) ) )

x = ( ratios_regal_to_other_spending .
      reset_index() .
      sort_values( [0] ) .
      reset_index()
      [0] )

plt.semilogy(x)
plt.grid( True )
plt.savefig( "reg-to-other-spending.png" )
plt.close()


######
###### Ratios of regalias spending to regalias income
######

regalias = pd.read_csv( "output/regalias.csv" )

def muni_regal_income( muni_code : int,
                       year : int ) -> float:
  return (
    regalias[
      (regalias["muni code"] == muni_code) &
      (regalias["year"]      == year) ]
    ["regalias"] . iloc[0] )

def regal_spending_to_regal_income(
    muni_code : int,
    year : int ) -> float:
  return ( regalias_spending_sum( muni_code, year )
           / muni_regal_income(     muni_code, year) )

def two_year_regal_spending_to_regal_income(
    muni_code : int,
    year : int ) -> float:
  return ( ( regalias_spending_sum( muni_code, year ) +
             regalias_spending_sum( muni_code, year+1 ) )
           / (2 * muni_regal_income(     muni_code, year) ) )

ratios = (
  spacetime_redundant .
  groupby( ["muni code","year"] ) .
  apply( ( lambda row:
           regal_spending_to_regal_income(
             row["mc"], row["yr"] ) ) ) )


ratios_2_year = (
  spacetime_redundant[
    spacetime_redundant[year] .
    isin( [2013,2015,2017] ) ] .
  # groupby( ["muni code","year"] ) .
  apply( ( lambda row:
           print( row );
           two_year_regal_spending_to_regal_income( row["mc"],
                                        row["yr"] ) ),
         axis = "columns" ) )

plt.semilogy(
  ratios_2_year.sort_values().reset_index(drop=True) )
plt.grid( True )
plt.savefig( "cdf.png" )


######
###### Time-series analysis of munis observed every year
######

def regalias_spending_sums_over_time(
    muni_code : int
    ) -> pd.Series:
  des = pd.DataFrame()
  for year in range(2013,2019):
    df = reg_gastos_by_year[year]
    df = df[ df["muni code"] == muni_code ]
    year_mean = pd.Series( [df["item oblig"].sum()] )
    year_mean.name = year
    des = pd.concat(
      [des, year_mean],
      axis = "columns",
      sort = True ) # because initially des has no rows
  res = des.iloc[0]
  res.name = muni_code
  return res

long_observed = (
  years_observed[
    years_observed["one"] > 5 ] .
  reset_index() ) # we need the index to be a column too
long_observed.index = long_observed["muni code"]

long_regalias_spending_sums_over_time = (
  long_observed .
  apply( ( lambda row:
           regalias_spending_sums_over_time(
             row["muni code"] ) ),
         axis = "columns" ) )

