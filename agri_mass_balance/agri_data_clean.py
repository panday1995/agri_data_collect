""" Nitrogen balance
Created on Jun 20 2022
@author: Fan Yang

ToDo
- read in all necessary files
- distribute nutrient across faostat harvest area
- generate .csv file that store nitrogen balance for crops

"""

from utilities_agri import Fert_data

def column_select(df, column_head, column_value):
    """
    This function is used for FAO stat to select rows based on column_value 

    Parameters
    ----------
        df: DataFrame, imported dataframe from FAO data
        column_head: str, column head in FAO data
        column_value: any, column value to be selected

    return
    ------
        df_selected: DataFrame, a dataframe with selected column values.
    """
    df_selected = df.loc[df[column_head]==column_value]
    return df_selected

crop_prod_by_country_FAO_df = Fert_data().read_crop_prod_by_country()
# area_harv_by_country_FAO_df = column_select(crop_prod_by_country_FAO_df,"Element","Area harvested")

fert_input_by_country_df = Fert_data().read_fert_input_by_country()
fert_use_by_country_df = column_select(fert_input_by_country_df,"Element","Agricultural Use")

N_input_rate_by_crop_country_df = Fert_data().read_N_input_rate()

area_harv_by_crop_country_IFA_df = Fert_data().read_crop_area_IFA()

