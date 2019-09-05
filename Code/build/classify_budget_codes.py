from typing import List, Dict, Set


def invert_set_dict(
    sd : Dict[ "k", Set["e"]]
    ) -> Dict[ "e", "k" ]:
  acc = dict()
  for k in sd.keys():
    for e in sd[k]:
      acc[e] = k
  return acc

if True: # test it
  assert (
    invert_set_dict( { "a" : {1,2},
                       "b" : {3,4} } )
    == { 1:"a", 2:"a", 3:"b", 4:"b"} )

if True: # some terms I don't want to misspell
  funcionamiento = "funcionamiento"
  inversion = "inversion"

if True: # our own aggregate categories
  personal = "Generales de personal"
  ambiental = "Ambiental"
  salud = "Salud"
  edu = "Educación"
  pension = "Pensiones"
  salario = "Salario alcalde, gobernador, concejales, diputados"
  segur = "Seguridad y justicia"
  gen = "Generales funcionamiento"
  otros = "Otros gastos sociales"
  infra = "Infraestructura y vivienda"
  pub = "Servicios publicos"
  cult = "Deporte, recreación y cultura"
  agro = "Agropecuario"

if True: # define map from aggregate categories to the codes comprising them
  categs_to_codes = { funcionamiento : {},
                   inversion : {} }
  if True: # for the funcionamiento files
    categs_to_codes[funcionamiento] = {}
    categs_to_codes[funcionamiento][personal] = { "1.1.1.1", "1.1.1.10", "1.1.1.14", "1.1.1.2", "1.1.1.25", "1.1.1.3", "1.1.1.4", "1.1.1.5", "1.1.1.7.1", "1.1.1.8", "1.1.1.9", "1.1.2", "1.1.3.1", "1.1.3.2", "1.1.3.3", "1.1.3.4", "1.1.3.5", "1.1.3.6", "1.1.3.7", "1.1.3.8", "1.1.4.1.1.1.1", "1.1.4.1.1.1.2", "1.1.4.1.1.1.3", "1.1.4.1.1.1.4", "1.1.4.1.1.3.1", "1.1.4.1.1.3.2", "1.1.4.1.1.4.1", "1.1.4.1.1.4.2", "1.1.4.2.1.1.1", "1.1.4.2.1.1.2", "1.1.4.2.1.1.3", "1.1.4.2.1.1.4", "1.1.4.2.1.3.1", "1.1.4.2.1.3.2", "1.1.4.2.1.4.1", "1.1.4.2.1.4.2", "1.1.4.3.1.1", "1.1.4.3.1.2", "1.1.4.3.2.1", "1.1.4.3.2.2", "1.1.4.3.3.1", "1.1.4.3.3.2", "1.1.4.3.4.1", "1.1.4.3.4.2", "1.1.4.3.5.1", "1.1.4.3.5.2", "1.1.5", "1.9.1.1", "1.9.1.2" }
    categs_to_codes[funcionamiento][ambiental] = {"1.3.8.1; 1.3.8.2; 1.3.9"}
    categs_to_codes[funcionamiento][edu] = {"1.3.6.1.1", "1.3.6.4.1", "1.3.6.4.6"}
    categs_to_codes[funcionamiento][pension] = {"1.1.4.1.1.2.1","1.1.4.1.1.2.2", "1.1.4.2.1.2.1", "1.1.4.2.1.2.2", "1.3.1", "1.3.12.1", "1.3.12.2", "1.3.2", "1.3.20", "1.3.3", "1.3.4.1", "1.3.4.2", "1.3.6.4.4"}
    categs_to_codes[funcionamiento][salario] = {"1.1.1.12", "1.1.1.6"}
    categs_to_codes[funcionamiento][segur] = {"1.3.6.7.1"}
    categs_to_codes[funcionamiento][gen] = {"1.10", "1.2.1.1", "1.2.1.2", "1.2.1.9", "1.2.2.10", "1.2.2.11", "1.2.2.12.1", "1.2.2.12.2", "1.2.2.12.5", "1.2.2.19", "1.2.2.2", "1.2.2.3.1", "1.2.2.3.2.1", "1.2.2.3.2.2", "1.2.2.3.2.3", "1.2.2.3.2.5", "1.2.2.3.2.9", "1.2.2.3.3", "1.2.2.3.4", "1.2.2.3.5", "1.2.2.4", "1.2.2.5", "1.2.2.6.1", "1.2.2.6.2", "1.2.2.6.3", "1.2.2.6.4", "1.2.2.6.5", "1.2.2.7", "1.2.2.8.1", "1.2.2.8.2", "1.2.2.8.3", "1.2.2.9", "1.2.4", "1.2.9", "1.3. 22", "1.3.10", "1.3.13", "1.3.14", "1.3.15", "1.3.18.1", "1.3.18.2", "1.3.18.3", "1.3.18.4", "1.3.19", "1.3.23", "1.3.24", "1.3.25", "1.3.6.5", "1.3.6.6", "1.3.6.7.10", "1.3.7", "1.4.1", "1.4.2", "1.4.3", "1.9.2.1", "1.9.2.2", "1.9.2.3", "1.9.2.4", "1.9.2.5", "1.9.2.6", "1.9.2.7", "1.9.2.8", "1.9.3", "1.9.4"}
    categs_to_codes[funcionamiento][infra] = {"1.3.11"}
  if True: # and for the inversion files
    categs_to_codes[inversion][ambiental] = {"A.10"}
    categs_to_codes[inversion][salud] = {"A.2"}
    categs_to_codes[inversion][edu] = {"A.1"}
    categs_to_codes[inversion][segur] = {"A.11", "A.18"}
    categs_to_codes[inversion][gen] = {"}A.17", "A.19"}
    categs_to_codes[inversion][otros] = {"A.12", "A.13", "A.14", "A.16"}
    categs_to_codes[inversion][infra] = {"A.9", "A.7", "A.15"}
    categs_to_codes[inversion][pub] = {"A.3", "A.6"}
    categs_to_codes[inversion][cult] = {"A.4", "A.5"}
    categs_to_codes[inversion][agro] = {"A.8"}

if True: # the inverse map: from (spending) budget codes to our aggregate categories
  codes_to_categs = {
    inversion      : invert_set_dict(
      categs_to_codes[inversion] ),
    funcionamiento : invert_set_dict(
      categs_to_codes[funcionamiento] ) }
  assert not set.intersection(
      set( codes_to_categs[inversion]      .keys() ),
      set( codes_to_categs[funcionamiento] .keys() ) )
  codes_to_categs = ( # This creates the union of the two dictioaries.
    dict( codes_to_categs[inversion],
          **codes_to_categs[funcionamiento] ) )
  assert codes_to_categs["A.8"] == agro
  assert codes_to_categs["1.1.1.1"] == personal
