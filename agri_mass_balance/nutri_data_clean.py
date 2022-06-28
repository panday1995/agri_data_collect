""" Nutrient data clean
Created on Jun 20 2022
@author: Fan Yang

This script 
- read in all necessary files from FAO and IFA
- 

ToDo
- IFA data time format
- IFA 
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

fert_input_by_country_df = Fert_data().read_fert_input_by_country() # read fertilizer data from FAO
fert_use_by_country_df = column_select(fert_input_by_country_df,"Element","Agricultural Use") # get fertilizer use data from FAO
N_use_by_country_df = fert_use_by_country_df.loc[
    fert_use_by_country_df.index.get_level_values("Item")=="Nutrient nitrogen N (total)"
] # get nitrogen use in FAOstat

N_input_rate_by_crop_country_df = Fert_data().read_N_input_rate() # read nitrogen input rate from IFA
area_harv_by_crop_country_IFA_df = Fert_data().read_crop_area_IFA() # read harvested area from IFA
N_input_by_crop_country_df = Fert_data().read_N_input() # read nitrogen input from IFA

N_input_by_crop_country_df = (1000 * # transfer from kt to t
                            N_input_by_crop_country_df.fillna(0).rename( # fill na values with 0
                            columns={"N_k_t":"value"} # rename column as value
                        ) 
                    )

