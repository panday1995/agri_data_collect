""" utility functions for agriculture module
Created on Jun 20 2022

@author Fan Yang

ToDO
- import fertlizer use data   
- rearrange fertilizer use data by country and crop into data point

"""



from importlib.resources import path
import os
import pandas as pd
import pathlib

class Fert_data:
    def __init__(self) -> None:
        super().__init__()    
        self.parent_path = pathlib.Path(__file__).parent.parent.resolve()
        self.data_path = os.path.join(self.parent_path,"data")

        self.faostat_data_path = os.path.join(self.data_path, "faostat")
        self.crop_prod_by_country = "Production\Production_Crops_Livestock_E_All_Data_(Normalized)\Production_Crops_Livestock_E_All_Data_(Normalized).csv"
        self.fert_input_by_country = "Land, Inputs and Sustainability\Inputs_FertilizersNutrient_E_All_Data_(Normalized)\Inputs_FertilizersNutrient_E_All_Data_(Normalized).csv"

        self.nutri_data_path = os.path.join(self.data_path, "nutri_data")       
        self.fert_input = "Global_data_on_fertilizer_use_2022.csv"

    def read_FAO_csv(self, fao_csv_path):
        df = pd.read_csv(fao_csv_path,
            encoding = "ISO-8859-1",
            index_col=[
                # "Area Code",
                "Area", # countries and regions
                #"Item Code",
                "Item", # crops
                #"Element Code",
                # "Element",
                # "Year Code",
                "Year", # year
                # "Unit",
                # "Flag",
            ]
        )
        return df

    def read_crop_prod_by_country(self):
        crop_prod_by_country_df = self.read_FAO_csv(
            os.path.join(self.faostat_data_path, self.crop_prod_by_country),
        )
        crop_prod_by_country_df = crop_prod_by_country_df.loc[:,["Element","Value"]]
        return crop_prod_by_country_df

    def read_fert_input_by_country(self):
        fert_input_by_country_df = self.read_FAO_csv(
            os.path.join(self.faostat_data_path, self.fert_input_by_country),
        )
        fert_input_by_country_df = fert_input_by_country_df.loc[:,["Element","Value"]]
        return fert_input_by_country_df

    def read_fert_input_by_crop_country(self):
        fert_input_by_crop_country_df = pd.read_csv(
            os.path.join(self.nutri_data_path, self.fert_input), 
            encoding = "ISO-8859-1",  
            ).drop(columns=[
                'Original_country_name_in_FUBC_report', # Original name of country used in Fertilizer use by crop (FUBC) report
                'Region_IFA', # Region, based on the International Fertilizer Association (IFA) list of aggregate countries and regions
                'FUBC_report_number',
                'Year_FUBC_publication', # The fertilizer use by crop (FUBC) report, year of publication
            ])

        # change year_format from t/t+1 or t-t+1 to t    
        year_ls = []
        for year in fert_input_by_crop_country_df["Year"]:
            if ("-" not in year) and ("/" not in year):
                year_ls.append(int(year))
            else:
                year_ls.append(int(year[:4]))
        fert_input_by_crop_country_df["Year"] = year_ls

        fert_input_by_crop_country_df.set_index(
            [
                # 'ISO3_code', # The 3-letter ISO3 United Nations code to signify country or region. Note that China, Taiwan was given the TWN 3-letter code                 
                'Country', # Country name based on official United Nations English name, with the exception that references to Belgium-Luxembourg were converted to 'Belgium', and China, Taiwan was converted to China, Taiwan
                'Year', # "Year in which the data relates to. Year is in character format because in some reports the data relate to non-calendar years e.g. 1991/92, 1997-98. These therefore include a mixture of calendar and 'crop' years
                'Crop', # Crop type, based on those originally reported in the fertilizer use by crop (FUBC) reports
                ],
                inplace=True,
        )
        fert_input_by_crop_country_df.index.rename([
                # "ISO3_code", #
                "Area", # rename Country as Area
                "Year", # rename Year as Year
                "Item", # reanme Crop as Item
                ], 
                inplace = True)
        return fert_input_by_crop_country_df

    def read_N_input_rate(self):
        fert_input_by_crop_country_df = self.read_fert_input_by_crop_country()
        N_input_rate_by_crop_country_df = fert_input_by_crop_country_df.loc[:,["N_rate_kg_ha"]]
        return N_input_rate_by_crop_country_df

    def read_N_input(self):
        fert_input_by_crop_country_df = self.read_fert_input_by_crop_country()
        N_input_by_crop_country_df = fert_input_by_crop_country_df.loc[:,["N_k_t"]]
        return N_input_by_crop_country_df

    def read_P2O5_input_rate(self):
        fert_input_by_crop_country_df = self.read_fert_input_by_crop_country()
        P2O5_input_by_crop_country_df = fert_input_by_crop_country_df.loc[:,["P2O5_rate_kg_ha"]]
        return P2O5_input_by_crop_country_df

    def read_K2O_input_rate(self):
        fert_input_by_crop_country_df = self.read_fert_input_by_crop_country()
        K2O_input_by_crop_country_df = fert_input_by_crop_country_df.loc[:,["K2O_rate_kg_ha"]]
        return K2O_input_by_crop_country_df

    def read_crop_area_IFA(self):
        fert_input_by_crop_country_df = self.read_fert_input_by_crop_country()
        crop_area_by_crop_country_df = fert_input_by_crop_country_df.loc[:,["Crop_area_k_ha"]]
        return crop_area_by_crop_country_df