# Some terms for spending or income items are too long
# to show without overlapping their neighbors in certain contexts.
# This inserts newlines into them, so they fit.

import Code.metadata.terms as t

remap = {
  "Otros" : "Otros",

  # spending
  t.personal    : "Salarios de\nfuncionarios",
  t.ambiental   : "Ambiental",
  t.salud       : "Salud",
  t.edu         : "Educación",
  t.pension     : "Pensiones",
  t.segur       : "Seguridad\n y justicia",
  t.gen         : "Generales\nfuncionamiento",
  t.otros       : "Otros gastos\nsociales",
  t.infra       : "Infraestructura\ny vivienda",
  t.pub         : "Servicios\npúblicos",
  t.cult        : "Deporte\nrecreación\ncultura",
  t.agro        : "Agropecuario",
  t.deuda_gasto : "Pago de\nla deuda",

  # income
  t.propios     : "Impuestos y\notros recursos\npropios*",
  t.transfer    : "Transferencias\ndel Gobierno\nNacional",
  t.capital     : """Dinero sobrante de\naños anteriores y otros\ningresos financieros*""",
  t.regalias    : "Regalías"
}
