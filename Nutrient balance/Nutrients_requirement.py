"""
Created on Jun 20 2022

@author: Fan Yang

ToDO
- Check crops included in faostat data

"""

import os
import pandas as pd
import pathlib

parent_path = pathlib.Path(__file__).parent.parent.resolve()
data_path = os.path.join(parent_path,"Nutrient balance")
faostat_data_path = os.path.join(data_path, "faostat")


