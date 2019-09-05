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

