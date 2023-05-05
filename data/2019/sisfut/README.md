# getting this data

## the easy way

An encrypted .zip file containing these reports is available here:

https://livejaverianaedu-my.sharepoint.com/:u:/g/personal/brown-j_javeriana_edu_co/EZDtLGI_18pGm114STmE-8gBOvQU1i-NDccjosFUfJZPLw?e=vABAlI

Extract it by running
`openssl enc -aes-256-cbc -d -in muni-reports.zip.enc -out muni-reports.zip2`
and then providing the password
`mil6NIbD6gQiF`

(It was created via
`openssl enc -aes-256-cbc -salt -in muni-reports.zip -out muni-reports.zip.enc`
The only reason it's encrypted is to prevent OneDrive from re-compressing using a format that my Linux installation cannot uncompress.)


## the hard way, straight from DNP

### first, download .xlsx files

The files were downloaded, at some length, from
https://sisfut.dnp.gov.co/
via to the following process:

* If the site asks for a login, choose the anonymous option.
* From the sidebar, choose Reporte FUT, and under that, Categoria.
* Download each of the following categories:
    * FUT_GASTOS_DE_INVERSION
    * FUT_GASTOS_FUNCIONAMIENTO
      and below that "Gastos de Funcionamiento", not "Transferencias"
    * FUT_INGRESSO
      and below that "Reporte", not "Transferencias"
    * FUT_INDICADORES_DE_CALIDAD
	  and below that "Definitivo"
	* FUT_DEUDA_PUBLICA
	  and below that "Creditos",
	  not "Creditos por sector" or "Renta Pignorada"
* Download the "last quarter" of each year. (It actually represents the entire year's activity.)
* Under "cargue", choose Definitivo.
* Leave department and municipality unspecified.

### then convert them to .csv

In the latest tax.co docker container
(jeffreybbrown/tax.co:2019-07-22.xlsx2csv),
xlsx2csv is already installed.
If you're in another environment,
first install it, via `easy_install xlsx2csv`.

Then run the included script `to_csv.sh`.
