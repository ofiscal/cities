# PURPOSE: Evaluate the completeness of the 2022 CUIPO data,
# starting with whether it has all munis and depts,
# and whether the Áreas Metropolitanas can safely be ignored.

import pandas as pd
from   typing import List, Dict, Set
#
from   Code.explore.cuipo.load import (build_3, g, i, g22, i22, jc, geo)
from   Code.explore.cuipo.lib import my_describe
