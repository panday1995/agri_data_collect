"""
Created on Jun 20 2022

@author Fan Yang

ToDO
- import fertlizer use data   
- rearrange fertilizer use data by country and crop into data point

"""



import os
import pandas as pd
import pathlib

class Fert_data_set(self):
    def __init__(self) -> None:
        super().__init__()    
        self.parent_path = pathlib.Path(__file__).parent.parent.resolve()
        self.data_path = os.path.join(parent_path,"data")

        self.faostat_data_path = os.path.join(data_path, "faostat")
        self.nutri_data_path = os.path.join(data_path, "nutri_data")

        self.fert_input = "Global_data_on_fertilizer_use_2022.csv"

    def read_fert_input(self.file_path, self.file_name):
        fert_input_df = pd.read_csv(os.path.join(self.file_path, self.file_name), encoding = "ISO-8859-1")
        return fert_input_df

    def 