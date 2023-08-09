from   typing import Set, List, Dict
from   os import path
import pandas as pd


#######################################################
# Remove the "big categories" column (ingreso or gasto),
# and reorders columns and rows.

data_root = "Code/explore/cuipo/concepto_keys/cuipo/observatorio-aggregates"

i = pd.read_excel (
  path.join ( data_root,
              "orig-xlsx",
              "ingresos.xlsx" ) )
i["item code"] = i["item code"] . astype(str)
i = ( i [[ "observatorio name",
           "item code",
           "item",
          ]]
      . sort_values ( [ "observatorio name",
                        "item code"] ) )

g = pd.read_excel (
  path.join ( data_root,
              "orig-xlsx",
              "gastos.xlsx" ) )
g["item code"] = g["item code"] . astype(str)
g = ( g [[ "observatorio name",
           "item code",
           "item",
          ]]
      . sort_values ( [ "observatorio name",
                        "item code" ] ) )


###################################################
#### Filter "gastos" to retain only the leaves ####

def is_leaf ( df : pd.DataFrame,
              s : str ) -> bool:
  return ( df["item code"]
           . apply ( lambda c :
                     c.startswith(s) )
           . astype ( int )
           . sum()
           == 1 )

def children ( df : pd.DataFrame,
               s : str ) -> List[str]:
  return [ c
           for c in set ( df["item code"] ) # TODO ? Pre-calculate for speed?
           if c.rpartition(".")[0] == s ]

def gastos_category ( df : pd.DataFrame,
                      s : str ) -> str:
  return ( df [ df["item code"] == s ]
           ["observatorio name"]
           . iloc[0] ) # works because each item code should be unique

def all_children_are_leaves_classified_like_parent (
    df : pd.DataFrame,
    p : str ) -> bool:
  parent_cat = gastos_category(df,p)
  cs = children(df,p)
  if not cs: return False
  if not ( df [ df["item code"] . isin(cs) ]
           ["is leaf"] . all() ):
    return False
  return ( pd.Series ( [ gastos_category(df,c) == parent_cat
                         for c in cs ] )
           . all () )


#### TODO : Fold the following code into a loop.
# The algorithm at work is to find all parents whose children are all leaves
# and classified the same way as the parent,
# delete those children,
# then redefine "leaf" and repeat.
# Once doing that results in no change,
# the process is complete.


g["is leaf"] = g["item code"] . apply ( lambda s :
                                        is_leaf(g,s) )
g["uniform parent"] = (
  g["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g,s) ) )

to_delete = [
  inner
  for outer in ( g[ g["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g,s) ) )
  for inner in outer ]

g1 = ( g [ ~ g ["item code"] . isin ( to_delete ) ]
       . copy() )

g.equals(g1)


### stupid -- roll this into a loop

g1["is leaf"] = g1["item code"] . apply ( lambda s :
                                          is_leaf(g1,s) )
g1["uniform parent"] = (
  g1["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g1,s) ) )

to_delete = [
  inner
  for outer in ( g1[ g1["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g1,s) ) )
  for inner in outer ]

g2 = ( g1 [ ~ g1 ["item code"] . isin ( to_delete ) ]
       . copy() )

g1.equals(g2)



### stupid -- roll this into a loop

g2["is leaf"] = g2["item code"] . apply ( lambda s :
                                          is_leaf(g2,s) )
g2["uniform parent"] = (
  g2["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g2,s) ) )

to_delete = [
  inner
  for outer in ( g2[ g2["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g2,s) ) )
  for inner in outer ]

g3 = ( g2 [ ~ g2 ["item code"] . isin ( to_delete ) ]
       . copy() )

g2.equals(g3)


### stupid -- roll this into a loop

g3["is leaf"] = g3["item code"] . apply ( lambda s :
                                          is_leaf(g3,s) )
g3["uniform parent"] = (
  g3["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g3,s) ) )

to_delete = [
  inner
  for outer in ( g3[ g3["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g3,s) ) )
  for inner in outer ]

g4 = ( g3 [ ~ g3 ["item code"] . isin ( to_delete ) ]
       . copy() )

g3.equals(g4)


### stupid -- roll this into a loop

g4["is leaf"] = g4["item code"] . apply ( lambda s :
                                          is_leaf(g4,s) )
g4["uniform parent"] = (
  g4["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g4,s) ) )

to_delete = [
  inner
  for outer in ( g4[ g4["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g4,s) ) )
  for inner in outer ]

g5 = ( g4 [ ~ g4 ["item code"] . isin ( to_delete ) ]
       . copy() )

g4.equals(g5)


### stupid -- roll this into a loop

g5["is leaf"] = g5["item code"] . apply ( lambda s :
                                          is_leaf(g5,s) )
g5["uniform parent"] = (
  g5["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g5,s) ) )

to_delete = [
  inner
  for outer in ( g5[ g5["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g5,s) ) )
  for inner in outer ]

g6 = ( g5 [ ~ g5 ["item code"] . isin ( to_delete ) ]
       . copy() )

g5.equals(g6)

### stupid -- roll this into a loop

g6["is leaf"] = g6["item code"] . apply ( lambda s :
                                          is_leaf(g6,s) )
g6["uniform parent"] = (
  g6["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g6,s) ) )

to_delete = [
  inner
  for outer in ( g6[ g6["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g6,s) ) )
  for inner in outer ]

g7 = ( g6 [ ~ g6 ["item code"] . isin ( to_delete ) ]
       . copy() )

g6.equals(g7)

### stupid -- roll this into a loop

g7["is leaf"] = g7["item code"] . apply ( lambda s :
                                          is_leaf(g7,s) )
g7["uniform parent"] = (
  g7["item code"]
  . apply ( lambda s:
            all_children_are_leaves_classified_like_parent(g7,s) ) )

to_delete = [
  inner
  for outer in ( g7[ g7["uniform parent"] ]["item code"]
                 . apply ( lambda s: children(g7,s) ) )
  for inner in outer ]

g8 = ( g7 [ ~ g7 ["item code"] . isin ( to_delete ) ]
       . copy() )

g7.equals(g8)


########################
#### Write the data ####

i.to_csv ( path.join ( data_root,
                       "ingresos.csv" ),
           index = False )
g8.to_csv ( path.join ( data_root,
                        "gastos.csv" ),
           index = False )
