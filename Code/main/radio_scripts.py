if True:
  import pandas as pd
  from   pathlib import Path
  import Code.common as c
  from   Code.main.geo import depts_and_munis

root = "output/pivots/recip-" + str(c.subsample)

def write_script(
    dept : str,
    muni : str,
    muni_code : int,
    ingresos : pd.DataFrame,
    gastos   : pd.DataFrame ):
  with open( root + "/" + dept + "/" + muni + "/radio.md",
             "w" ) as f:
    f.write( "\n\n".join( [
      "Píldora municipal para " + muni + ", " + dept + "(Código DANE: " + str(muni_code) + ")",
      "Recuerde: su voto determina en manos de quién van a quedar los recursos de " + muni + ". Por eso es importante que conozca de dónde viene la plata su municipio y cómo la gastan sus gobernantes." ] ) )

# More text, yet to incorporate
"Mi nombre es Luis Carlos Reyes y soy el director del Observatorio Fiscal de la Universidad Javeriana. Con el fin de que usted pueda conocer cómo se usan los recursos de su municipio, el Observatorio ha preparado un análisis de lo que pasa con este dinero, para que usted evalúe el uso que la alcaldía y el concejo municipal les dan a los recursos públicos."

"¿Sabía que el año pasado el gobierno de " + muni + " contó con recursos de $" + total_muni_income_2018 + "? Este es el dinero con el cual se pueden financiar servicios como el transporte escolar de sus hijos,  la construcción de vías terciarias para llevar productos desde las fincas hasta el mercado, la atención médica y las adecuaciones a los hospitales del municipio."

"Durante este gobierno, el " + fraction_income_transfers_since_2015 + "% de los recursos del municipio vinieron de transferencias del Gobierno Nacional, y el " + fraction_income_regalias_since_2015 + "% de las regalías que se obtuvieron por la explotación petrolera y minera. Si bien estos recursos no provienen de los impuestos pagados por los habitantes del municipio, son suyos y es responsabilidad del alcalde y el concejo administrarlos responsablemente y para el beneficio de todos."

"Además, alrededor de " + [[PERCENTAGE OF TAX INCOME 2015-2018, NO % SIGN]] + " de cada 100 pesos que le entraron a " + muni + " vienen de impuestos que pueden ser aumentados o reducidos por el alcalde y el Concejo, como el impuesto predial que se les puede cobrar a los dueños de fincas y casas, o el ICA que se les puede cobrar a los negocios. El concejo municipal y el alcalde pueden decidir si subir o bajar estos impuestos 

En el Observatorio Fiscal de la Universidad Javeriana nuestra tarea es que tenga insumos suficientes para definir su voto, y apoyarlo con su tarea de conocer cómo se reparte la torta de los ingresos en su municipio. Así que aquí le contamos que el principal gasto de " + muni + " durante esta administración ha sido en salud, pues se ha invertido un " + fraction_spending_health_since_2015 + " del presupuesto del municipio; se ha invertido el " fraction_spending_housing_since_2015 + " en infraestructura y vivienda, y el " + fraction_spending_edu_since_2015 + " en educación."

"Como ciudadano de " + muni + ", usted conoce mejor que nadie si estos recursos se están empleando adecuadamente. ¿Qué promesas están haciendo los candidatos? ¿Sí alcanza la plata para lo que están prometiendo? ¿Qué gastos tendrían que recortar para financiar lo que prometen, o qué impuestos tendrían que subir? Su voto define cómo se manejarán los recursos de su municipio. Exíjales cuentas claras a los candidatos al concejo y a la alcaldía este 27 de octubre y, ante todo, vote."

depts_and_munis.apply(
  ( lambda row:
    write_script( dept = row["dept"],
                  muni = row["muni"],
                  muni_code = 0,
                  gastos = 0,
                  ingresos = 0 ) ),
  axis = "columns" )

( Path( root + "/" + "timestamp-for-radio" ) .
  touch() )

