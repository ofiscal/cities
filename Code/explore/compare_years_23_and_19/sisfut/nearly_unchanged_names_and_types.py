from typing import List, Dict, GenericAlias
import os.path as path
import pandas as pd
import numpy as np
#
import Code.explore.compare_years_23_and_19.lib as lib


(vao19,vao23) = lib.compare_views_from_2019_and_2023 ("ingresos")
(vao19,vao23) = lib.compare_views_from_2019_and_2023 ("funcionamiento")
(vao19,vao23) = lib.compare_views_from_2019_and_2023 ("inversion")
