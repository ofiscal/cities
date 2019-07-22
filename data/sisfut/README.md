# getting this data

## the easy way

A .zip file containing these reports is available here:
https://livejaverianaedu-my.sharepoint.com/:u:/g/personal/brown-j_javeriana_edu_co/ERqNUO8cpEhKs64nvuyRBOIBx7On3G2LQ2u3-f7dn-1rvw?e=NBoOKw


## the hard way, straight from DNP

### first, download .xlsx files

The files were downloaded, at some length, from
https://sisfut.dnp.gov.co/
via to the following process:

* From the sidebar, choose Reporte FUT, and under that, Categoria.
* Download each of the following categories:
    * FUT_GASTOS_DE_INVERSION
    * FUT_GASTOS_FUNCIONAMIENTO
    * FUT_INGRESOS
    * FUT_INDICADORES_DE_CALIDAD
* Download the "last quarter" of each year. (It actually represents the entire year's activity.)
* Under "cargue", choose Definitivo.
* Leave department and municipality unspecified.

### then convert them to .csv

(This can be done from within the docker container, or outside.)

First install xlsx2csv, by running `easy_install xlsx2csv`.

Then run the included script `to_csv.sh`.
