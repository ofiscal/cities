# The two products of interest in this are
# codes_to_categs     : Dict[ code, categ ]
# categs_to_code_sets : Dict[ categ, Set[code] ]
# of_interest         : Dict[ "gastos"|"ingresos", Set[code] ]

from typing import List, Dict, Set
import Code.metadata.terms as t


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

def invert_many_to_one_dict (d : Dict["x","y"]
                             ) -> Dict["y",Set["x"]]:
  acc = {}
  for k in d.keys():
    v = d[k]
    if v in acc.keys():
      acc[v] = set.union( acc[v], {k} )
    else: acc[v] = {k}
  return acc

if True: # test it
  assert ( invert_many_to_one_dict( {1:1,2:1,3:4} )
           == {1:{1,2},4:{3}} )

if True: # define map from aggregate categories to the codes comprising them
  categs_to_codes = { t.funcionamiento : {},
                      t.inversion : {},
                      t.ingresos : {},
                      t.deuda : {} }
  if True: # for the funcionamiento files
    categs_to_codes[t.funcionamiento] = {}

    categs_to_codes[t.funcionamiento][t.personal] = {
      "1.1.1.1",
      "1.1.1.10",
      "1.1.1.12",
      "1.1.1.14",
      "1.1.1.2",
      "1.1.1.25",
      "1.1.1.3",
      "1.1.1.4",
      "1.1.1.5",
      "1.1.1.6",
      "1.1.1.7.1",
      "1.1.1.8",
      "1.1.1.9",
      "1.1.2",
      "1.1.3.1",
      "1.1.3.2",
      "1.1.3.3",
      "1.1.3.4",
      "1.1.3.5",
      "1.1.3.6",
      "1.1.3.7",
      "1.1.3.8",
      "1.1.4.1.1.1.1",
      "1.1.4.1.1.1.2",
      "1.1.4.1.1.1.3",
      "1.1.4.1.1.1.4",
      "1.1.4.1.1.3.1",
      "1.1.4.1.1.3.2",
      "1.1.4.1.1.4.1",
      "1.1.4.1.1.4.2",
      "1.1.4.2.1.1.1",
      "1.1.4.2.1.1.2",
      "1.1.4.2.1.1.3",
      "1.1.4.2.1.1.4",
      "1.1.4.2.1.3.1",
      "1.1.4.2.1.3.2",
      "1.1.4.2.1.4.1",
      "1.1.4.2.1.4.2",
      "1.1.4.3.1.1",
      "1.1.4.3.1.2",
      "1.1.4.3.2.1",
      "1.1.4.3.2.2",
      "1.1.4.3.3.1",
      "1.1.4.3.3.2",
      "1.1.4.3.4.1",
      "1.1.4.3.4.2",
      "1.1.4.3.5.1",
      "1.1.4.3.5.2",
      "1.1.5",
      "1.9.1.1",
      "1.9.1.2",
    }

    categs_to_codes[t.funcionamiento][t.ambiental] = {
      "1.3.8.1",
      "1.3.8.2",
      "1.3.9",
    }

    categs_to_codes[t.funcionamiento][t.edu] = {
      "1.3.6.1.1",
      "1.3.6.4.1",
      "1.3.6.4.6",
    }
    categs_to_codes[t.funcionamiento][t.pension] = {
      "1.1.4.1.1.2.1",
      "1.1.4.1.1.2.2",
      "1.1.4.2.1.2.1",
      "1.1.4.2.1.2.2",
      "1.3.1",
      "1.3.12.1",
      "1.3.12.2",
      "1.3.2",
      "1.3.20",
      "1.3.3",
      "1.3.4.1",
      "1.3.4.2",
      "1.3.6.4.4",
    }

    categs_to_codes[t.funcionamiento][t.segur] = {"1.3.6.7.1"}

    categs_to_codes[t.funcionamiento][t.gen] = {
      "1.2.1.1",
      "1.2.1.2",
      "1.2.1.9",
      "1.2.2.10",
      "1.2.2.11",
      "1.2.2.12.1",
      "1.2.2.12.2",
      "1.2.2.12.5",
      "1.2.2.19",
      "1.2.2.2",
      "1.2.2.3.1",
      "1.2.2.3.2.1",
      "1.2.2.3.2.2",
      "1.2.2.3.2.3",
      "1.2.2.3.2.5",
      "1.2.2.3.2.9",
      "1.2.2.3.3",
      "1.2.2.3.4",
      "1.2.2.3.5",
      "1.2.2.4",
      "1.2.2.5",
      "1.2.2.6.1",
      "1.2.2.6.2",
      "1.2.2.6.3",
      "1.2.2.6.4",
      "1.2.2.6.5",
      "1.2.2.7",
      "1.2.2.8.1",
      "1.2.2.8.2",
      "1.2.2.8.3",
      "1.2.2.9",
      "1.2.4",
      "1.2.9",
      "1.3.10",
      "1.3.13",
      "1.3.14",
      "1.3.15",
      "1.3.18.1",
      "1.3.18.2",
      "1.3.18.3",
      "1.3.18.4",
      "1.3.19",
      "1.3.22",
      "1.3.23",
      "1.3.24",
      "1.3.25",
      "1.3.6.5",
      "1.3.6.6",
      "1.3.6.7.10",
      "1.3.7",
      "1.4.1",
      "1.4.2",
      "1.4.3",
      "1.9.2.1",
      "1.9.2.2",
      "1.9.2.3",
      "1.9.2.4",
      "1.9.2.5",
      "1.9.2.6",
      "1.9.2.7",
      "1.9.2.8",
      "1.9.3",
      "1.9.4"
      "1.10",
      }

    categs_to_codes[t.funcionamiento][t.infra] = {"1.3.11"}

  if True: # for the inversion files
    categs_to_codes[t.inversion][t.ambiental] = {"A.10"}
    categs_to_codes[t.inversion][t.salud] = {"A.2"}
    categs_to_codes[t.inversion][t.edu] = {"A.1"}
    categs_to_codes[t.inversion][t.segur] = {"A.11", "A.18"}
    categs_to_codes[t.inversion][t.gen] = {"A.17", "A.19"}
    categs_to_codes[t.inversion][t.otros] = {"A.12", "A.13", "A.14", "A.16"}
    categs_to_codes[t.inversion][t.infra] = {"A.9", "A.7", "A.15"}
    categs_to_codes[t.inversion][t.pub] = {"A.3", "A.6"}
    categs_to_codes[t.inversion][t.cult] = {"A.4", "A.5"}
    categs_to_codes[t.inversion][t.agro] = {"A.8"}
  if True: # for the ingresos files
    categs_to_codes[t.ingresos][t.propios] = {"TI.A"}
    categs_to_codes[t.ingresos][t.transfer] = {"TI.A.2.6"}
    categs_to_codes[t.ingresos][t.capital] = {"TI.B"}
  if True: # for the deuda files
    categs_to_codes[t.deuda][t.deuda_gasto] = {"T"}


if True: # the inverse map: from (spending) budget codes to our aggregate categories
  three_inverses = {
    t.inversion      : invert_set_dict(
      categs_to_codes[t.inversion] ),
    t.funcionamiento : invert_set_dict(
      categs_to_codes[t.funcionamiento] ),
    t.ingresos : invert_set_dict(
      categs_to_codes[t.ingresos] ),
    t.deuda : invert_set_dict(
      categs_to_codes[t.deuda] ) }
  assert not set.intersection(
      set( three_inverses[t.inversion]      . keys() ),
      set( three_inverses[t.funcionamiento] . keys() ),
      set( three_inverses[t.ingresos]       . keys() ),
      set( three_inverses[t.deuda]          . keys() ) )
  codes_to_categs = ( # This creates the union of the two dictioaries.
    dict(   three_inverses[t.inversion],
          **three_inverses[t.funcionamiento],
          **three_inverses[t.ingresos],
          **three_inverses[t.deuda] ) )
  assert codes_to_categs["A.8"]     == t.agro
  assert codes_to_categs["1.1.1.1"] == t.personal
  assert codes_to_categs["TI.B"]    == t.capital
  assert codes_to_categs["T"]       == t.deuda_gasto

categs_to_code_sets : Dict[ str, Set[str] ] = (
    invert_many_to_one_dict( codes_to_categs ) )

of_interest = {
  t.funcionamiento : set.union( *[
    categs_to_codes[t.funcionamiento][k]
    for k in categs_to_codes[t.funcionamiento].keys() ] ),
  t.inversion : set.union( *[
    categs_to_codes[t.inversion][k]
    for k in categs_to_codes[t.inversion].keys() ] ),
  t.ingresos : set.union( *[
    categs_to_codes[t.ingresos][k]
    for k in categs_to_codes[t.ingresos].keys() ] ),
  t.deuda : set.union( *[
    categs_to_codes[t.deuda][k]
    for k in categs_to_codes[t.deuda].keys() ] ) }
