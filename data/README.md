# "The cuipo" data

The Ofiscal knowledge graph notes on it are here:
https://github.com/ofiscal/knowledge-graph/blob/master/cuipo_data.org

This is data from a new system we're just learning about in 2023.
It may be what we have to use instead of SISFUT for later years,
because for most municipalities,
SISFUT appears only to be complete for years through 2020.

## The file `dept-and-muni-CHIPs.csv`

comes from Juan Camilo at the Contaduría,
emailed to Oliver on <2023-07-13 Thu>.

For an organized version of what he wrote,
see the note entitled
  Juan Camilo's response re. isolating munis and depts in CUIPO
in the repo
  https://github.com/JeffreyBenjaminBrown/secret-org

# "Vintage" matters

There are two vintages of data used --
one set of data downloaded in 2019, the other in 2023.
Both begin at 2013,
and extend as far into the future as SISFUT permitted at the time.

# The inflation data

## for 2019

comes from DANE,
specifically the most recent (as of today)
"Anexo" here:
https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/ipc-historico

## for 2023

is the inflation index EXCLUDING FOOD from the Central Bank --
which as of this commit was downloaded in March 2023.

# Why the data only goes back to 2013

There is no regalías data before that.

# Why there are 2019 and 2023 subdirectories

This project was first conceived in May of 2019,
and used to produce reports later that year,
using data from then.

With another election cycle looming in 2023,
I am resurrecting the project.
It will need new data,
which will be different not just in content but also in form.
To ensure correctness, the two data sets must be maintained in parallel,
so that they (and whatever they are used to create) can be compared.
