# PITFALL: This generates .txt files.
# Our radio team wants .docx files.
# To convert to .docx, use
# `Code/convert-to-docx-via-pandoc.sh`.

if True:
  import os
  import pandas as pd
  from   pathlib import Path
  #
  import Code.common as c
  import Code.draw.text.shorten_numbers as abbrev
  import Code.metadata.terms as t
  from   Code.main.geo import depts_and_munis


src_root = os.path.join ( c.outdata, "pivots",
                          "recip-" + str(c.subsample) )
dest     = os.path.join ( c.outdata, "radio",
                          "recip-" + str(c.subsample) )
if not os.path.exists( dest ):
  os.makedirs( dest )

def src_folder( dept : str,
                muni : str ) -> str:
  return os.path.join ( src_root, dept, muni )

def write_script(
    dept : str,
    muni : str,
    muni_code : int,
    ingresos_all_years  : pd.DataFrame,
    ingresos_recent_pct : pd.DataFrame,
    gastos_recent_pct   : pd.DataFrame ):
  print( dept + " / " + muni )
  total_muni_income_2018 = (
    abbrev.show_brief_with_units( round(
      ingresos_all_years["2018"].sum() ) ) )
  fraction_income_transfers_after_2015 = abbrev.show_brief(
    100 * ingresos_recent_pct[ t.transfer ], 0 )
  fraction_income_regalias_after_2015 = abbrev.show_brief(
    100 * ingresos_recent_pct[ t.regalias ], 0 )
  fraction_income_taxes_after_2015 = abbrev.show_brief(
    100 * ingresos_recent_pct[ t.propios ], 0 )
  fraction_spending_health_after_2015 = abbrev.show_brief(
    100 * gastos_recent_pct[ t.salud ], 0 )
  fraction_spending_health_after_2015 = abbrev.show_brief(
    100 * gastos_recent_pct[ t.salud ], 0 )
  fraction_spending_housing_after_2015 = abbrev.show_brief(
    100 * gastos_recent_pct[ t.infra ], 0 )
  fraction_spending_justice_after_2015 = abbrev.show_brief(
    100 * gastos_recent_pct[ t.segur ], 0 )
  fraction_spending_edu_after_2015 = abbrev.show_brief(
    100 * gastos_recent_pct[ t.edu ], 0 )

  print( "\n",
         total_muni_income_2018,
         fraction_income_transfers_after_2015,
         fraction_income_regalias_after_2015,
         fraction_income_taxes_after_2015,
         fraction_spending_health_after_2015,
         fraction_spending_health_after_2015,
         fraction_spending_housing_after_2015,
         fraction_spending_edu_after_2015 )

  dest_file = (
    os.path.join (
      dest,
      ( dept + "__" + muni
             + "_" + str(muni_code) + ".txt" ) )
    . replace( " ", "-" ) )

  with open( dest_file, "w" ) as f:
    f.write ( "\n\n".join( [
      "Píldora municipal para " + muni + ", " + dept + "(Código DANE: " + str(muni_code) + ")",
      "Recuerde: su voto determina en manos de quién van a quedar los recursos de " + muni + ". Por eso es importante que conozca de dónde viene la plata su municipio y cómo la gastan sus gobernantes.",
      "Mi nombre es Luis Carlos Reyes y soy el director del Observatorio Fiscal de la Universidad Javeriana. Con el fin de que usted pueda conocer cómo se usan los recursos de su municipio, el Observatorio ha preparado un análisis de lo que pasa con este dinero, para que usted evalúe el uso que la alcaldía y el concejo municipal les dan a los recursos públicos.",
      "¿Sabía que el año pasado el gobierno de " + muni + " contó con recursos de $" + total_muni_income_2018 + "? Este es el dinero con el cual se pueden financiar servicios como el transporte escolar de sus hijos,  la construcción de vías terciarias para llevar productos desde las fincas hasta el mercado, la atención médica y las adecuaciones a los hospitales del municipio.",
      "Durante este gobierno, el " + fraction_income_transfers_after_2015 + "% de los recursos del municipio vinieron de transferencias del Gobierno Nacional, y el " + fraction_income_regalias_after_2015 + "% de las regalías que se obtuvieron por la explotación petrolera y minera. Si bien estos recursos no provienen de los impuestos pagados por los habitantes del municipio, son suyos y es responsabilidad del alcalde y el concejo administrarlos responsablemente y para el beneficio de todos.",
      "Además, alrededor de " + fraction_income_taxes_after_2015 + " de cada 100 pesos que le entraron a " + muni + " vienen de impuestos que pueden ser aumentados o reducidos por el alcalde y el Concejo, como el impuesto predial que se les puede cobrar a los dueños de fincas y casas, o el ICA que se les puede cobrar a los negocios. El concejo municipal y el alcalde pueden decidir si subir o bajar estos impuestos.",
      "En el Observatorio Fiscal de la Universidad Javeriana nuestra tarea es que tenga insumos suficientes para definir su voto, y apoyarlo con su tarea de conocer cómo se reparte la torta de los ingresos en su municipio. Así que aquí le contamos que el gasto de " + muni + " en salud durante esta administración ha sido del " + fraction_spending_health_after_2015 + " del presupuesto del municipio; se ha invertido el " + fraction_spending_housing_after_2015 + " en infraestructura y vivienda, el " + fraction_spending_justice_after_2015 + " en seguridad y justicia, y el " + fraction_spending_edu_after_2015 + " en educación.",
      "Como ciudadano de " + muni + ", usted conoce mejor que nadie si estos recursos se están empleando adecuadamente. ¿Qué promesas están haciendo los candidatos? ¿Sí alcanza la plata para lo que están prometiendo? ¿Qué gastos tendrían que recortar para financiar lo que prometen, o qué impuestos tendrían que subir? Su voto define cómo se manejarán los recursos de su municipio. Exíjales cuentas claras a los candidatos al concejo y a la alcaldía este 27 de octubre y, ante todo, vote."
    ] ) )

depts_and_munis.apply(
  ( lambda row:
    write_script(
      dept = row["dept"],
      muni = row["muni"],
      muni_code = row["muni code"],
      ingresos_all_years = (
        pd.read_csv( src_folder( row["dept"],
                                 row["muni"] ) +
                     "/ingresos.csv" ) ),
      ingresos_recent_pct = (
        pd.read_csv( ( src_folder( row["dept"],
                                   row["muni"] ) +
                       "/ingresos-pct-compare.csv" ),
                     index_col = 0 ) .
        loc[:,row["muni"]] ),
      gastos_recent_pct = (
        pd.read_csv( ( src_folder( row["dept"],
                                   row["muni"] ) +
                       "/gastos-pct-ungrouped.csv"),
                     index_col = 0 ) .
        iloc[:,0] ) ) ),
  axis = "columns" )

( Path ( os.path.join ( dest,
                        "timestamp-for-radio" ) ) .
  touch () )
